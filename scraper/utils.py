import logging
import threading
import urllib2

import time

import itertools
from datetime import timedelta
from multiprocessing.dummy import Pool

import bs4
import cfscrape
import pymongo
from pymongo import MongoClient
from scraper.models import Trader

chrome_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'
HEADERS ={  # Add more user agents and use a random function to get them
    'User-Agent': chrome_agent,
}

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

PROXIES = {'http': '88.210.158.189:87',  # These ones are blocked
           'https': '46.231.117.154:90'
           }

DATA = dict(location='London', cat=20)


class Scraper:
    """
    Standard settings for Scrapers
    """

    def __init__(self):
        self.items = 0
        self.pages = 0
        self.time = 0
        self.memory = 0
        self.scraper = cfscrape.create_scraper()
        self.scraper.headers.update(HEADERS)
        # scraper.proxies.update(PROXIES)

    def show_stats(self):
        return " Scraped %s items in %s seconds." % self.items, self.time

    def get_url_page(self, url, retries=5):
        """

        :param url: Url of the page to scrape
        :return: Requests the page and returns its html content
        """
        try:
            if retries > 0:
                response = self.scraper.get(url)
                if response.status_code >= 500 and response.status_code < 600:
                    return self.get_url_page(url, self.scraper, retries-1)
                elif response.status_code >= 200 and response.status_code < 300:
                    return bs4.BeautifulSoup(response.content, "lxml")
                else:
                    return None
            else:
                return None
        except Exception, e:
            print "Something went wrong. %s" % e
            return None



class CheckATradeScraper(Scraper):
    MAIN_URL = "http://www.checkatrade.com"
    SEARCH_STRING = "/Search/?postcode=NW2+3RE&adaptive=True&location=London&sort=1&page=%s&facet_Category=20"


    def get_trader_list(self, html_page):
        """

        :param html_page: beautiful soup html page
        :return: list of traders from a page
        """
        results = html_page.find('ul', {'class': 'results'})
        for result in results.find_all('li'):
            yield result.h2.a.get('href')


    def get_info_itemprop(self, tag, _type, body):
        """
        Gets the information based on the itemprop of the tag.
        It assumes that all the fields have the correct item prop.


        :param tag: the html tag to parse
        :param _type: the type of the information
        :param body: the body of the code
        :return: the text or 'Not found'
        """
        try:
            info = body.find(tag, {'itemprop': _type})
            if _type == 'url':
                return info['href']
            return info.text
        except:
            return "Not found"

    def get_all_traders_list(self):
        """
        Gets all the traders from all the pages in a search with url.
        The total number of pages is determined on the first page by reading the nr of pages from pagination

        """
        url = self.MAIN_URL  + self.SEARCH_STRING % 1
        page_html = self.get_url_page(url)  # HTML for the first page
        self.pages = page_html.find('ul', {'class': 'pagination'}).find_all('li')[-3].find('a').text  # Finds the nr of page results
        for i in xrange(2, int(self.pages)):
            yield self.get_trader_list(page_html)
            url = self.MAIN_URL + self.SEARCH_STRING % i
            page_html = self.get_url_page(url)

    def get_trader_info(self,trader_url, local=False, db=None):
            logging.debug('Starting')
            # for trader_url in trader_list:
            html_page = self.get_url_page(self.MAIN_URL+trader_url, self.scraper)
            contacts = html_page.find('div',{'class': 'contact-card__details'})
            name = self.get_info_itemprop('h1', 'name', contacts)
            email = self.get_info_itemprop('a', 'email', contacts)
            url = self.get_info_itemprop('a', 'url', contacts)
            # if random() > 0.2:  # It only saves for some random pages to save memory
            #     html_page = ""
            trader_obj, created = Trader.objects.get_or_create(
                        name=name,
                        defaults={
                            'email': email,
                            'url': url,
                            'checkatrade_url': self.MAIN_URL+trader_url
                            # 'page': str(html_page),
                            }
                    )

    def __call__(self):
        """
        Triggers the scrapper.

        """
        init = time.time()
        traders_list = itertools.chain.from_iterable(self.get_all_traders_list())
        # pool = Pool(2)
        # pool.map(self.get_trader_info, traders_list)  # TODO: check back for tests and comparisons

        # A thread is in use here so the request can end without timeout. A sleep function should be used to avoid overusing the server
        t = threading.Thread(target=map, args=(self.get_trader_info, traders_list))
        # t1 = threading.Thread(target=self.get_trader_info, args=(traders_list,))
        t.daemon = True
        t.start()
        # t.join()
        self.time = time.time() - init


class CheckATradeLocalDB:
    """
    MongoDB to connect locally


    """
    def __init__(self, client=None, expires=timedelta(days=30)):
        self.client = client if client else MongoClient('localhost', 27017)
        self.db = self.client['checkatrade']
        self.db.plumbers.create_index([("name", pymongo.DESCENDING)], background=True)

    def insert_plumber(self, name, email, url):
        data = {
            'name': name,
            'email': email,
            'url': url
        }
        self.db.plumbers.update({'name': name}, { '$set': data})


    def get_plumber(self, name):
        """

        :param name: plumber's name
        :return: Returns the plumber name if it finds it in the db
        """
        result = self.db.plumbers.find_one({'name': name})
        if result:
            return result['name']
        else:
            return "Not found"

    def get_all_plumbers(self):
        for plumber in self.db.plumbers.find({}):
            yield plumber.name, plumber.email








