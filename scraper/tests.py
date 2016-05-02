import random
from unittest import TestCase

# Create your tests here.
# from django.test import TestCase
import re

from scraper.utils import CheckATradeScraper


class CheckATradeParserTest(TestCase):
    """
    Checks if the methods used to get the data still work for the current html structure
    """
    def setUp(self):
        self.scraper = CheckATradeScraper()
        url = self.scraper.MAIN_URL + self.scraper.SEARCH_STRING % 1  # TODO: choose a page at random
        self.results_html = self.scraper.get_url_page(url)
        self.refs_list = list(self.scraper.get_trader_list(self.results_html))

    def test_trader_href_list(self):
        """
        tests if the href has the right format

        """
        for ref in self.refs_list:
            self.assertTrue(re.search(r'^/\w+/$', ref))

    def test_page_info_format(self):
        """
        Checks if the info we're getting from the page is being scraped with the right format

        """
        url = self.refs_list[random.randint(0, len(self.refs_list)-1)]
        test_page = self.scraper.get_url_page(url)  # exchange this for a copy of an html file

        url_info = self.scraper.get_info_itemprop('a', 'url', test_page)
        self.assertTrue(re.search(r'^http://www.', url_info) or url_info == "Not found")

        email_info = self.scraper.get_info_itemprop('a', 'email', test_page)
        self.assertTrue(re.search(r'^\S+@\S+', email_info) or email_info == "Not found")

    def test_scraping_all_traders(self):
        """
        Checks if the scraper gets all the scrapers by comparing the total results on the site with the total pages scraped

        """
        pass

