from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from utils import scrape_checkatrade


# Create your views here.
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
        return {'objects': scrape_checkatrade() }




def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
