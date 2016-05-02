import logging

from django.db import models
from scraper.utils import CheckATradeScraper



class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s" % self.id


class Category(BaseModel):
    name = models.CharField(max_length=255)
    ref = models.IntegerField(default=20)


class Trader(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    checkatrade_url = models.URLField(help_text="Trader's location on checkatrade", default="")
    url = models.URLField(help_text="Trader's url")
    category = models.ForeignKey(Category, related_name="traders", blank=True, null=True)


    class Meta:
        ordering = ['-updated']

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
                            'url': url,
                            'checkatrade_url': self.MAIN_URL+trader_url
                            }
                    )



