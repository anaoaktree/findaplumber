from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from scraper.models import Trader, DjangoCheckATradeScraper

# Create your views here.
from scraper.utils import CheckATradeScraper


def index(request):
    """
    Main view for hello app

    :param request: Gets a request
    :return: Returns the homepage
    """
    # return HttpResponse('Hello from Python!')
    return redirect('show_plumbers')


class CheckATradeView(TemplateView):
    template_name = 'plumber_list.html'

    def get_context_data(self, **kwargs):
        ctx = {
            'objects': Trader.objects.all()
        }
        return ctx


class ScrapeCheckATradeView(View):

    def get(self, *args,**kwargs):
        sc = DjangoCheckATradeScraper()
        sc()  # Scrapes the website
        print "Scraped %s pages in  %s seconds" % (sc.pages, sc.time)
        return redirect('show_plumbers')

