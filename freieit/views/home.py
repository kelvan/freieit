from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout

from django.core.context_processors import csrf

from haystack.views import SearchView

class IndexSearchView(SearchView):

  # def __call__(self, request):
  #       """
  #       Generates the actual response to the search.

  #       Relies on internal, overridable methods to construct the response.
  #       """
  #       self.request = request

  #       self.form = self.build_form()
  #       self.query = self.get_query()
  #       self.results = self.get_results()

  #       return self.create_response()

  def get_query(self):
      """
      Returns the query provided by the user.

      Returns an empty string if the query is invalid.
      """
      if self.form.is_valid():
        import pdb; pdb.set_trace()
        # TODO wird das mehrmals aufgerufen?
        self.form.cleaned_data['q'] = self.form.cleaned_data['q'] + self.request.GET.get('tagname', '')
        return self.form.cleaned_data['q']

    
#SearchView

def show(request):
  return render_to_response('home.html')
