import logging
from random import randint, random

from django.db import models
from scraper.utils import CheckATradeScraper



class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s" % self.id
class Scraper(BaseModel):
    ref = models.CharField(max_length=255, default="checkatrade")
    results_page = models.TextField(blank=True, null=True)



class Category(BaseModel):
    name = models.CharField(max_length=255)
    ref = models.IntegerField(default=20)


class Trader(BaseModel):
    name = models.CharField(max_length=355)
    email = models.EmailField()
    checkatrade_url = models.URLField(help_text="Trader's location on checkatrade", default="",max_length=355)
    url = models.URLField(help_text="Trader's url")
    category = models.ForeignKey(Category, related_name="traders", blank=True, null=True)
    average_score = models.IntegerField(default=0)
    # html = models.TextField(default="", editable=False)
    page = models.TextField(default="", max_length=1000)
    trader = models.ForeignKey(Scraper, related_name="traders", null=True)

    class Meta:
        ordering = ['-updated']

    def __unicode__(self):
        return self.name



class DjangoCheckATradeScraper(CheckATradeScraper):
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



