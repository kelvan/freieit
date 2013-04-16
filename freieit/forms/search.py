from haystack.forms import SearchForm
from django import forms
import random
from freieit import models
from haystack.models import SearchResult

class ExpertSearchForm(SearchForm):
    q = forms.CharField(required=False,
                        label='', 
                        widget=forms.TextInput(
                            attrs={'placeholder': 'Wobei brauchen Sie Hilfe?',
                                   'id':'suchfeld'}))
    
    def __init__(self, *args, **kwargs):
        self.seed = kwargs.pop("seed")
        super(ExpertSearchForm, self).__init__(*args, **kwargs)
        
        
    def as_plain(self):
        "Returns this form rendered as HTML <div>s."
        return self._html_output(
            normal_row = u'%(field)s%(help_text)s',
            error_row = u'%s',
            row_ender = '',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = True)

    def no_query_found(self):
        # we do not use searchqueryset here because with ngramfields
        # all does not return any object
        # see https://groups.google.com/forum/?fromgroups#!topic/django-haystack/q1n6w6S5PJQ
        
        # this a quick hack: fake a searchresult list
        # Performance? (Double database access, sort as list in memory)
        # Since we have to switch the search backend anyway if the site grows
        # this should work as quick workaround
        # (premature optimization ist the root of all evil)
        
        random.seed(self.seed)
        def make_result(expert):
            return SearchResult(app_label="freieit",
                                pk=expert.id,
                                model_name="expertprofile",
                                score=random.random())
        all_ = map(make_result,
                   models.ExpertProfile.objects.filter(available=True))
        all_.sort(key=lambda o:o.score)
        return all_
