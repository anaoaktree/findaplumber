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
    main_url = models.URLField()
    search_string = models.CharField(max_length=255)
    results_page = models.TextField(blank=True, null=True)

    # def run(self):  # When the nr of sites should grow, apply a scalable way of doing this
    #     sc = DjangoCheckATradeScraper()
    #     sc()


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
