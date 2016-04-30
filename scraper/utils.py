import urllib2

import time

import itertools

import bs4
import cfscrape
import requests, mechanize
from requests.cookies import cookiejar_from_dict
from requests.packages.urllib3.connection import ConnectionError

chrome_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'

HEADERS ={
    'User-Agent': chrome_agent,

}

DATA = dict(location = 'London', cat=20)

def get_url_page(url, session, retries = 5):
    """

    :param url: Url of the page to scrape
    :return: Requests the page and returns its html content
    """
    try:
        if retries > 0:
            response = session.get(url)
            if response.status_code >= 500 and response.status_code < 600:
                return get_url_page(url, session, retries-1)
            elif response.status_code >= 200 and response.status_code < 300:
                return bs4.BeautifulSoup(response.content, "lxml")
            else:
                return None
        else:
            return None
    except Exception, e:
        print "Something went wrong. %s" %e
        return None



def get_trader_list(html_page):
    """

    :param html_page: beautiful soup html page
    :return: list of traders from a page
    """
    results = html_page.find('ul', {'class': 'results'})
    for result in results.find_all('li'):
        yield result.h2.a.get('href')


def get_info_itemprop(tag, type, body):
    try:
        return body.find(tag, {'itemprop': type}).text
    except:
        return "Not found"


def get_trader_info(url, traders_href_list, scraper):
    trader_url = traders_href_list.next()
    while trader_url:
        response = get_url_page(url+trader_url, scraper).find('div',{'class': 'contact-card__details'})
        yield get_info_itemprop('h1', 'name', response), get_info_itemprop('a', 'email', response), get_info_itemprop('a', 'url', response)
        trader_url = traders_href_list.next()

SEARCH_STRING = "/Search/?postcode=NW2+3RE&adaptive=True&location=London&sort=1&page=%s&facet_Category=20"

def get_all_traders_list(main_url, scraper):
    """
    Gets all the traders from all the pages in a search with url

    :param url:
    :param scraper:
    :return:
    """
    url = main_url + SEARCH_STRING % 1
    page_html = get_url_page(url, scraper)  # HTML for the first page
    # total_pages = page_html.find('ul', {'class':'pagination'}).find_all('li')[-3].find('a').text  # Finds the nr of page results
    total_pages = 3
    for i in xrange(2, int(total_pages)):
        yield get_trader_list(page_html)
        url = main_url + SEARCH_STRING % i
        page_html = get_url_page(url, scraper)



def scrape_checkatrade():
    main_url = "http://www.checkatrade.com"
    url = main_url + "/Search/?location=London&cat=20"

    scraper = cfscrape.create_scraper()
    traders_list = itertools.chain.from_iterable(get_all_traders_list(main_url, scraper))

    return get_trader_info(main_url, traders_list, scraper), time.clock()




