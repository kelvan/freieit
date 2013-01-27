from django.conf import settings
from django.conf.urls import patterns, include, url
from invitation.views import register
from django.contrib.auth.views import login, logout
from registration.forms import RegistrationFormTermsOfService
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from views.home import IndexSearchView
from haystack.forms import SearchForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

if getattr(settings, 'INVITE_MODE', False):
    urlpatterns = patterns('',
        url(r'^accounts/register/$',    register,
                                            {   
                                                'form_class': RegistrationFormTermsOfService,
                                                'backend': 'invitation.backends.InvitationBackend',
                                            },  
                                            name='registration_register'),
    )   
else:
    urlpatterns = patterns('',
        url(r'^accounts/register/$',    register,
                                            {   
                                                'form_class': RegistrationFormTermsOfService,
                                                'backend': 'registration.backends.default.DefaultBackend',
                                            },  
                                            name='registration_register'),
    )

urlpatterns += patterns('',
    url(r'^accounts/',              include('invitation.urls')),
    url(r'^accounts/',              include('registration.urls')),
    url(r'^admin/',                 include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += patterns('',
  url(r'^$', IndexSearchView(form_class=SearchForm, template="home.html"), name='haystack_search'),

  # url(r'^$', 'freieit.views.home.show'),
  url(r'^login$',                       'freieit.views.login.show'),
  url(r'^login$',                       login, name='login'),
  url(r'^accounts/login/$',             login),
  url(r'^logout$',                      logout),
  url(r'^accounts/logout/$',            logout, name='logout'),
  #url(r'^register$',                    'freieit.views.register.show'),
  url(r'^profile$',                     'freieit.views.profile.show'),
  url(r'^expert/(?P<expert>[\w_\-]+)$', 'freieit.views.expert.show'),
  url(r'^experts/(?P<page_num>\d+)?$',  'freieit.views.experts.show'),
  url(r'^map$',                         'freieit.views.map.show'),
  url(r'^map/rss.xml$',                 'freieit.views.map.rss'),
  url(r'^tag/(?P<tag>[\w_\-]+)/(?P<page_num>\d+)?', 'freieit.views.tag.show'),
)

# static templates
urlpatterns += patterns('',
  url(r'^about/$', direct_to_template, {'template': 'about.htm'}),
  url(r'^dienste/$', direct_to_template, {'template': 'dienste.htm'}),
  url(r'^tipps/$', direct_to_template, {'template': 'tipps.htm'}),
  url(r'^statuten/$', direct_to_template, {'template': 'statuten.htm'}),
  url(r'^impressum/$', direct_to_template, {'template': 'impressum.htm'})
)

if settings.DEBUG:
  urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
      'document_root': settings.MEDIA_ROOT,
    }),
  )

urlpatterns += staticfiles_urlpatterns()
