import re

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout

from django.core.context_processors import csrf

from haystack.views import SearchView
from copy import copy
from taggit.models import Tag

class IndexSearchView(SearchView):
  def build_form(self, form_kwargs=None):
    """
    Instantiates the form the class should use to process the search query.
    """
    data = None
    kwargs = {
      'load_all': self.load_all,
      }
    if form_kwargs:
      kwargs.update(form_kwargs)
      
    if len(self.request.GET):
      data = self.request.GET.copy()
      tag = data.get('tagname', None)
      if tag and not tag in data['q']:
        data['q'] = data['q'] + " " + re.sub(r'[^\w ]', '', tag) 
        
    if self.searchqueryset is not None:
      kwargs['searchqueryset'] = self.searchqueryset
          
    return self.form_class(data, **kwargs)

  def extra_context(self):
    return dict(tags=Tag.objects.all())



def show(request):
  return render_to_response('home.html')