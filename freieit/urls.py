from django.conf import settings
from django.conf.urls import patterns, include, url
from invitation.views import register
from django.contrib.auth.views import login, logout
from registration.forms import RegistrationFormTermsOfService

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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
  (r'^search/', include('haystack.urls')),

  url(r'^$', 'freieit.views.home.show'),
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

if settings.DEBUG:
  urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
      'document_root': settings.MEDIA_ROOT,
    }),
  )

urlpatterns += staticfiles_urlpatterns()
