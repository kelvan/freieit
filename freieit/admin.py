from django.contrib import admin
from models import *

admin.site.register(ExpertProfile, ExpertProfileAdmin)
admin.site.register(Link, LinkAdmin)
