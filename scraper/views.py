from django.shortcuts import render
from django.views.generic import TemplateView, View
from scraper.models import Trader


# Create your views here.
from scraper.utils import CheckATradeScraper


def index(request):
    """
    Main view for hello app

    :param request: Gets a request
    :return: Returns the homepage
    """
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


class CheckATradeView(TemplateView):
    template_name = 'plumber_list.html'

    def get_context_data(self, **kwargs):
        ctx = {
            'objects': Trader.objects.all()
        }
        return ctx


class ScrapeCheckATradeView(CheckATradeView):

    def get_context_data(self, **kwargs):
        CheckATradeScraper()  # Scrapes the website
        super(self, ScrapeCheckATradeView).get_context_data( **kwargs)

