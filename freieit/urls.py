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

  #url(r'^', 'freieit.views.'),
  url(r'^$',                  'freieit.views.experts.show'),
  url(r'^(?P<page_num>\d+)$', 'freieit.views.experts.show'),
  url(r'^login',              'freieit.views.login.show'),
  url(r'^register',           'freieit.views.register.show'),
  url(r'^terms_of_business',  'freieit.views.terms_of_business.show'),
  url(r'^become_expert',      'freieit.views.become_expert.show'),
  url(r'^contact',            'freieit.views.contact.show'),
  url(r'^free_software',      'freieit.views.free_software.show'),
  url(r'^tips_and_tricks',    'freieit.views.tips_and_tricks.show'),
  url(r'^faq',                'freieit.views.faq.show'),
  url(r'^links',              'freieit.views.links.show'),
  url(r'^tag/(?P<tag>\w+)',   'freieit.views.tag.show'),

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
