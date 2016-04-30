import urllib2

import time

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


COOKIES = {'.ASPXANONYMOUS':'pJh-6RnY0QEkAAAAOWRhMGY5NmYtNTk3NC00ZTNiLWIyYWEtZTI1YTA5ODg0ZWNm7Kygg8vTHbjLkWInPO0oRc8DYH9b6nA3sRhQst_8Tic1',
           'cf_clearance':'d7fa3b3224e2574ef10b38aa855c10901bd24b19',
           '__cfduid':'d210d11ebab28912abff4157a6dd1a8b21461873396',
           'LastSearch':'Lat=&Lon=&Category=20&Location=London&URL=http%3a%2f%2fwww.checkatrade.com%2fSearch%2fdefault.aspx%3flocation%3dLondon%26cat%3d20',
           '_ga':'GA1.2.1412154492.1461873401',
           '_dc_gtm_UA':'1'
}


def get_url_page(url, session, retries = 5):
    """

    :param url: Url of the page to scrape
    :return: Requests the page and returns its html content
    """
    try:
        if retries > 0:
            response = session.get(url)
            # session.cookies.update(response.cookies)
            if response.status_code >= 500 and response.status_code < 600:
                return get_url_page(url, session, retries-1)
            elif response.status_code >= 200 and response.status_code < 300:
                return bs4.BeautifulSoup(response.content)
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
    for trader_url in traders_href_list:
        response = get_url_page(url+trader_url, scraper).find('div',{'class': 'contact-card__details'})
        yield get_info_itemprop('h1', 'name', response), get_info_itemprop('a', 'email', response), get_info_itemprop('a', 'url', response)


def scrape_checkatrade():
    main_url = "http://www.checkatrade.com"
    url = main_url + "/Search/?location=London&cat=20"
    # resul = download(url)
    # with requests.Session() as sess:
    #     sess.headers.update(HEADERS)
    #     # session.cookies.update(cookiejar_from_dict(COOKIES))
    scraper = cfscrape.create_scraper()
    page = get_url_page(url, scraper)
    traders_list = get_trader_list(page)
    return get_trader_info(main_url, traders_list, scraper)




