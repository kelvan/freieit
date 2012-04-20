from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class Tag(models.Model):
  tag = models.CharField(max_length=512)

  class Meta:
      verbose_name = _('Tag')
      verbose_name_plural = _('Tags')
      ordering = ['tag']

  def __str__(self):
    return self.tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    search_fields = ('tag',)

class ExpertProfile(models.Model):

  # the user this expert profile is associated with
  user = models.ForeignKey(User, unique=True)

  # the experts name
  name = models.CharField(max_length=512, null=True, blank=True)

  # experts image
  image = models.ImageField(upload_to="expert_images")

  # phone number of the expert
  phone = models.CharField(max_length=256)

  # the services this expert offers
  services = models.CharField(max_length=2048)

  # location where the services can be offered
  location = models.CharField(max_length=2048)

  # time when the services can be offered
  time = models.CharField(max_length=2048)

  # charges for this expert
  charges = models.CharField(max_length=2048)

  # tags for this expert
  keywords = models.ManyToManyField(Tag)

  class Meta:
      #unique_together = (("user", "name"),)
      verbose_name = _('Expert Profile')
      verbose_name_plural = _('Expert Profiles')
      ordering = ['name']

  def __str__(self):
    return self.name

class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'location')
    list_filter = ('location', 'keywords')
    search_fields = ('name', 'location', 'services')
