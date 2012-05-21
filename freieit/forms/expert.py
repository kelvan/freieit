from django.forms import ModelForm
from freieit.models import ExpertProfile

class ExpertProfileForm(ModelForm):
    class Meta:
        model = ExpertProfile
        exclude = ('user', 'editor')
