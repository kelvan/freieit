from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.contrib import admin

from .views.home import IndexSearchView
from .views import NewExpertView, ExpertView
from .forms.search import ExpertSearchForm


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(
        r'^robots\.txt$', lambda r: HttpResponse(
            "User-agent: *\nDisallow: /", mimetype="text/plain")
    ),
    url(r'expert/(?P<pk>\d+)', ExpertView.as_view(), name='expert'),
    url(
        r'^$', IndexSearchView(
            form_class=ExpertSearchForm, template='home.html'
        ), name='haystack_search'
    ),
    url(r'^newexpert$', NewExpertView.as_view()),
]

# static templates
urlpatterns += [
    # TODO replace with flatpages
    url(r'^about/$', TemplateView.as_view(template_name='about.htm')),
    url(r'^dienste/$', TemplateView.as_view(template_name='dienste.htm')),
    url(r'^tipps/$', TemplateView.as_view(template_name='tipps.htm')),
    url(r'^statuten/$', TemplateView.as_view(template_name='statuten.htm')),
    url(r'^impressum/$', TemplateView.as_view(template_name='impressum.htm'))
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
    urlpatterns += staticfiles_urlpatterns()
