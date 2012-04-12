from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
  tag = models.CharField(max_length=512)

class ExpertProfile(models.Model):

  # the user this expert profile is associated with
  user = models.ForeignKey(User, unique=True)

  # the experts name
  name = models.CharField(max_length=512)

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




