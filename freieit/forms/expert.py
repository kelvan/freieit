from django import forms
from django.forms import ModelForm
from freieit.models import ExpertProfile

class ExpertProfileForm(ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = ExpertProfile
        exclude = ('user', 'editor', 'available')
