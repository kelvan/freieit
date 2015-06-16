from django import forms
from django.forms import ModelForm

from .models import ExpertProfile


class ExpertProfileForm(ModelForm):
    email = forms.EmailField(max_length=30)
    terms = forms.BooleanField()
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = ExpertProfile
        exclude = ('user', 'editor', 'available')
