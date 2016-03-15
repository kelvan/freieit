from django import forms
from django.forms.models import inlineformset_factory
from django.forms import ModelForm

from ..models import ExpertProfile, Link


class ExpertProfileForm(ModelForm):
    email = forms.EmailField(max_length=30)
    terms = forms.BooleanField()
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = ExpertProfile
        exclude = ('user', 'editor', 'available')


class LinkForm(ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Link
        exclude = []


LinkFormSet = inlineformset_factory(
    ExpertProfile, Link, form=LinkForm, can_delete=False
)
