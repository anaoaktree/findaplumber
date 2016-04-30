from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import scraper.views
from scraper.views import CheckATradeView,ScrapeCheckATradeView

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', scraper.views.index, name='index'),
    url(r'^plumbers/$', CheckATradeView.as_view(), name='show_plumbers'),
    url(r'^plumbers/scrape/$', ScrapeCheckATradeView.as_view(), name='scrape_checkatrade'),
    # url(r'^db', scraper.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
