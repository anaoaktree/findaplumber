import logging
import threading
import urllib2

import time

import itertools

import bs4
import cfscrape
import requests, mechanize
from requests.cookies import cookiejar_from_dict
from requests.packages.urllib3.connection import ConnectionError
from scraper.models import Trader

chrome_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'

HEADERS ={
    'User-Agent': chrome_agent,

}

# logging.basicConfig(level=logging.DEBUG,
#                     format='[%(levelname)s] (%(threadName)-10s) %(message)s',
#                     )

PROXIES = {'http': '88.210.158.189:87',
           'https': '46.231.117.154:90'
           }

DATA = dict(location = 'London', cat=20)


class Scraper:
    """
    Standard settings for Scrapers
    """

    def __init__(self):
        self.items = 0
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
            print "Something went wrong. %s" %e
            return None



class CheckATradeScraper(Scraper):
    MAIN_URL = "http://www.checkatrade.com"
    SEARCH_STRING = "/Search/?postcode=NW2+3RE&adaptive=True&location=London&sort=1&page=%s&facet_Category=20"


    def get_trader_list(self,html_page):
        """

        :param html_page: beautiful soup html page
        :return: list of traders from a page
        """
        results = html_page.find('ul', {'class': 'results'})
        for result in results.find_all('li'):
            yield result.h2.a.get('href')


    def get_info_itemprop(self,tag, _type, body):
        try:
            info = body.find(tag, {'itemprop': _type})
            if _type == 'url':
                return info['href']
            return info.text
        except:
            return "Not found"


    def get_trader_info(self,url, traders_href_list, max_threads=2):
        # trader_url = traders_href_list.next()
        # def info_queue():
        for trader_url in traders_href_list:
            # logging.debug('Starting')
            response = self.get_url_page(url+trader_url, self.scraper).find('div',{'class': 'contact-card__details'})
            trader_obj, created = Trader.objects.update_or_create(
                name=self.get_info_itemprop('h1', 'name', response),
                defaults={
                    'email': self.get_info_itemprop('a', 'email', response),
                    'url': self.get_info_itemprop('a', 'url', response)
                    }
            )


    def get_all_traders_list(self,main_url):
        """
        Gets all the traders from all the pages in a search with url

        :param url:
        :param scraper:
        :return:
        """
        url = main_url + self.SEARCH_STRING % 1
        page_html = self.get_url_page(url)  # HTML for the first page
        # total_pages = page_html.find('ul', {'class':'pagination'}).find_all('li')[-3].find('a').text  # Finds the nr of page results
        total_pages = 3
        for i in xrange(2, int(total_pages)):
            yield self.get_trader_list(page_html)
            url = main_url + self.SEARCH_STRING % i
            page_html = self.get_url_page(url)



    def scrape_checkatrade(self):

        traders_list = itertools.chain.from_iterable(self.get_all_traders_list(self.MAIN_URL))
        self.get_trader_info(self.MAIN_URL, traders_list)




