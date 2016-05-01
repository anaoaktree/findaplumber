import argparse
import logging
import threading

import itertools

from scraper.utils import CheckATradeLocalDB, CheckATradeScraper
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
class CheckATradeLocalScraper(CheckATradeScraper):
    def get_trader_info(self, traders_list, db):
        logging.debug('Starting')
        for trader_url in traders_list:
            response = self.get_url_page(self.MAIN_URL+trader_url, self.scraper).find('div',{'class': 'contact-card__details'})
            name = self.get_info_itemprop('h1', 'name', response)
            email = self.get_info_itemprop('a', 'email', response)
            url = self.get_info_itemprop('a', 'url', response)
            db.insert_plumber(name, email, url)
            logging.debug('Inserted to mongo %s %s %s' % (name, email, url))

    def __call__(self,db):
        traders_list = itertools.chain.from_iterable(self.get_all_traders_list())
        t = threading.Thread(target=self.get_trader_info, args=(traders_list, db))
        t.daemon = True
        t.start()
        t.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape plumber information')
    parser.add_argument('-u', '--update', dest='update', action='store_true', help='Scrapes the site and updates the local db')
    parser.add_argument('-s', '--show', dest='show', action='store_true', help='Prints the current db records')
    parser.add_argument('-csv', '--to-csv', dest='csv', action='store_true', help='Saves the information to a csv file')  # TODO dawnload to csv
    args = parser.parse_args()
    db = CheckATradeLocalDB()
    if args.update:
        sc = CheckATradeLocalScraper()
        sc(db)
    for pl in db.get_all_plumbers():  # TODO: FIX MONGO DB
        print pl
    print db.get_plumber("GL Service & Installation")


    # Add timestamp to mongo db lib and one more useful field from checkatrade
    # Write tests
    # Track preformance