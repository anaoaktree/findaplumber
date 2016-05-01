import logging

from django.db import models
from oaktree.core.abstract_models import TitleAndSlugModel, BaseModel
from scraper.utils import CheckATradeScraper


class Category(TitleAndSlugModel):
    ref = models.IntegerField(default=20)


class Trader(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    url = models.URLField()
    category = models.ForeignKey(Category, related_name="traders", blank=True, null=True)

    def __unicode__(self):
        return self.name


class DjangoCheckATradeScraper(CheckATradeScraper):
    def get_trader_info(self,trader_url, local=False, db = None):
            logging.debug('Starting')
            # for trader_url in trader_list:
            response = self.get_url_page(self.MAIN_URL+trader_url, self.scraper).find('div',{'class': 'contact-card__details'})
            name = self.get_info_itemprop('h1', 'name', response)
            email = self.get_info_itemprop('a', 'email', response)
            url = self.get_info_itemprop('a', 'url', response)
            if local and db: # Saves in local db
                db.insert_plumber(name, email, url)
                logging.debug('Inserted to mongo %s' % ((name, email, url)))
            else: # Saves in django model
                trader_obj, created = Trader.objects.update_or_create(
                        name=name,
                        defaults={
                            'email': email,
                            'url': url
                            }
                    )



