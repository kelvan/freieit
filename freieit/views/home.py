from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout

from django.core.context_processors import csrf

from haystack.views import SearchView
from copy import copy

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
      tag = data['tagname']
      if not tag in data['q']:
        data['q'] = data['q'] + " " + tag 
        
    if self.searchqueryset is not None:
      kwargs['searchqueryset'] = self.searchqueryset
          
    return self.form_class(data, **kwargs)




def show(request):
  return render_to_response('home.html')
