import time

from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from scraper.models import Trader
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
    """
    Returns the list of all the current Plumbers
    """
    template_name = 'plumber_list.html'

    def get_context_data(self, **kwargs):
        ctx = {
            'objects': Trader.objects.all()
        }
        return ctx


class ScrapeCheckATradeView(View):

    def get(self, *args, **kwargs):
        sc = CheckATradeScraper()
        sc()  # Scrapes the website
        time.sleep(10)  # Allows time to refresh the page
        return redirect('show_plumbers')

