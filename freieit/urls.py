from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Examples:
  # url(r'^$', 'freieit.views.home', name='home'),
  # url(r'^freieit/', include('freieit.foo.urls')),

  (r'^search/', include('haystack.urls')),

  #url(r'^', 'freieit.views.'),
  #url(r'^$',                  'freieit.views.experts.show'),
  #url(r'^(?P<page_num>\d+)?$',                'freieit.views.experts.show'),
  url(r'^login$',             'freieit.views.login.show'),
  url(r'^logout$',            'freieit.views.login.do_logout'),
  url(r'^register$',          'freieit.views.register.show'),
  url(r'^profile$',           'freieit.views.profile.show'),
  url(r'^expert/(?P<expert>[\w_\-]+)$',          'freieit.views.expert.show'),
  url(r'^map$',               'freieit.views.map.show'),
  url(r'^map/rss.xml$',       'freieit.views.map.rss'),
  # FIXME merge next 2 regex
  #url(r'^tag/(?P<tag>\w+)',                   'freieit.views.tag.show'),
  url(r'^tag/(?P<tag>[\w_\-]+)/(?P<page_num>\d+)?', 'freieit.views.tag.show'),

  # Uncomment the admin/doc line below to enable admin documentation:
  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
      'document_root': settings.MEDIA_ROOT,
    }),
  )

urlpatterns += staticfiles_urlpatterns()
