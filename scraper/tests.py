

from unittest import TestCase

# Create your tests here.
from scraper.utils import CheckATradeScraper


class CheckATradeParserTest(TestCase):
    """
    Checks if the methods used to get the data still work for the current html structure
    """

    def setUp(self):
        self.scraper = CheckATradeScraper()


    def test_trader_href_list(self,html):
        """

        :param html:  Html page to get the urls from
        :return:
        """
        ref = self.scraper.get_trader_list(html)


