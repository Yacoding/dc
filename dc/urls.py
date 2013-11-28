from django.conf.urls import patterns, include, url
from dc import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('dc.views',
	url(r'^$', 'index'),
    url(r'^time/$', 'current_datetime'),
    url(r'^time/plus/(\d{1,2})$', 'hours_ahead'),
    # Examples:
    # url(r'^$', 'dc.views.home', name='home'),
    # url(r'^dc/', include('dc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

# scrawpy module's route configure
urlpatterns += patterns('scraper.views',
    url(r'^scraper/$', 'scraper_index'),
    url(r'^scraper/admin/$', 'scraper_admin'),
    url(r'^scraper/crawl/$', 'crawl'),
    url(r'^scraper/category/$', 'category'),
    url(r'^scraper/download/$', 'get_excel'),
    url(r'^scraper/monitor/$', 'monitor'),
)


# products module's route configure
urlpatterns += patterns('products.views',
    url(r'^radar/$', 'radar_index'),
    url(r'^radar/detail/$', 'radar_detail'),
    url(r'^radar/selectProducts$', 'select_products'),
    url(r'^radar/getCategory$', 'get_category'),
    url(r'^radar/test/$', 'test'),
)


# schedule module's route configure
urlpatterns += patterns('schedule.views',
    url(r'^schedule/$', 'schedule_index'),
    url(r'^schedule/run$', 'run'),
    url(r'^schedule/stop$', 'stop'),
)


# statis files' route configure
urlpatterns += patterns('',
	url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_ROOT}),
	url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_ROOT}),
	url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMG_ROOT}),
)