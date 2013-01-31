from haystack.forms import SearchForm
from django import forms


class ExpertSearchForm(SearchForm):
    q = forms.CharField(required=False,
                        label='', 
                        widget=forms.TextInput(attrs={'placeholder': 'Wobei brauchen Sie Hilfe?',
                                                      'id':'suchfeld'}))
    def as_plain(self):
        "Returns this form rendered as HTML <div>s."
        return self._html_output(
            normal_row = u'%(field)s%(help_text)s',
            error_row = u'%s',
            row_ender = '',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = True)

    def no_query_found(self):
        return self.searchqueryset.all()
