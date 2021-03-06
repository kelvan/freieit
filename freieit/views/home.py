from django.shortcuts import render

from haystack.views import SearchView
from ..models import Tag

PER_PAGES = [5, 10, 25, 50]


class IndexSearchView(SearchView):
    results_per_page = 50

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {'load_all': self.load_all}
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET.copy()
            if "results_per_page" in data:
                self.results_per_page = int(data['results_per_page'])

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        try:
            self.seed = self.request.COOKIES['seed']
        except KeyError:
            self.seed = "-".join(filter(None, map(
                self.request.META.get,
                ['HTTP_USER_AGENT', 'REMOTE_ADDR', 'REMOTE_HOST'])))

        kwargs['seed'] = self.seed
        return self.form_class(data, **kwargs)

    def create_response(self):
        response = super(IndexSearchView, self).create_response()
        response.set_cookie("seed", self.seed)
        return response

    @property
    def results_per_page_ix(self):
        return PER_PAGES.index(self.results_per_page)

        def extra_context(self):
            def ix(delta):
                newix = max(self.results_per_page_ix + delta, 0)
                if newix > len(PER_PAGES)-1:
                    newix = len(PER_PAGES) - 1
                return PER_PAGES[newix]

            # XXX
            return {'tags': Tag.objects.all(),
                    'paginate_down': ix(-1),
                    'paginate_up': ix(1),
                    'clsup': "off" if self.results_per_page_ix == len(PER_PAGES) - 1 else "",
                    'clsdown': "off" if self.results_per_page_ix == 0 else ""
                    }


def show(request):
    return render(request, 'home.html')
