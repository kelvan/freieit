from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.contrib import admin

from invitation.views import register
from registration.forms import RegistrationFormTermsOfService

from .views.home import IndexSearchView
from .forms.search import ExpertSearchForm

admin.autodiscover()

if getattr(settings, 'INVITE_MODE', False):
    urlpatterns = patterns('',
                           url(r'^accounts/register/$', register,
                               {
                                   'form_class': RegistrationFormTermsOfService,
                                   'backend': 'invitation.backends.InvitationBackend',
                               },
                               name='registration_register'),
                           )
else:
    urlpatterns = patterns('',
                           url(r'^accounts/register/$', register,
                               {
                                   'form_class': RegistrationFormTermsOfService,
                                   'backend': 'registration.backends.default.DefaultBackend',
                               },
                               name='registration_register'),
                           )

urlpatterns += patterns('',
                        url(r'^accounts/',
                            include('invitation.urls')),
                        url(r'^accounts/',
                            include('registration.urls')),
                        url(r'^admin/',
                            include(admin.site.urls)),
                        url(r'^admin/doc/',
                            include('django.contrib.admindocs.urls')),
                        (r'^robots\.txt$', lambda r: HttpResponse(
                            "User-agent: *\nDisallow: /", mimetype="text/plain"))
                        )

urlpatterns += patterns('',
                        url(r'^$', IndexSearchView(
                            form_class=ExpertSearchForm, template="home.html"), name='haystack_search'),
                        url(r'^newexpert$',
                            'freieit.views.newexpert.show'),
                        )

# static templates
urlpatterns += patterns('',
                        url(r'^about/$', direct_to_template,
                            {'template': 'about.htm'}),
                        url(r'^dienste/$', direct_to_template,
                            {'template': 'dienste.htm'}),
                        url(r'^tipps/$', direct_to_template,
                            {'template': 'tipps.htm'}),
                        url(r'^statuten/$', direct_to_template,
                            {'template': 'statuten.htm'}),
                        url(r'^impressum/$', direct_to_template,
                            {'template': 'impressum.htm'})
                        )

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                            }),
                            )

urlpatterns += staticfiles_urlpatterns()
