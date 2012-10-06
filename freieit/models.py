from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from audited_models.models import AuditedModel
from choices import LABELS, COUNTRIES, CURRENCIES

class ExpertProfile(AuditedModel):
    # the user this expert profile is associated with
    user = models.ForeignKey(User)

    # the experts name
    name = models.CharField(max_length=512, null=True, blank=True)

    # experts image
    image = models.ImageField(upload_to="expert_images")

    # the services this expert offers
    services = models.CharField(max_length=2048)

    # location of expert
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    city = models.CharField(max_length=30)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=2, choices=COUNTRIES)

    # time when the services can be offered
    time = models.CharField(max_length=1024)

    # charges for this expert
    charges = models.PositiveIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES, null=True, blank=True)
    charges_details = models.TextField(null=True, blank=True)

    # tags for this expert
    keywords = TaggableManager()

    class Meta:
            #unique_together = (("user", "name"),)
            verbose_name = _('Expert Profile')
            verbose_name_plural = _('Expert Profiles')
            ordering = ['name']

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.user.get_full_name()

    @property
    def address(self):
        return "%s %s, %s %s, %s" % (self.street, self.number, self.postcode, self.city, self.country)

    @property
    def price(self):
        return "%s %s" % (self.currency, self.charges)

    def get_absolute_url(self):
        return "/expert/%s" % self.user.username
        
class Link(AuditedModel):
    expert = models.ForeignKey(ExpertProfile)
    label = models.CharField(max_length=20, choices=LABELS)
    url = models.CharField(max_length=200)

class LinkInline(admin.TabularInline):
    model = Link

class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'address', 'price')
    list_filter = ('country', 'city', 'keywords__name')
    search_fields = ('name', 'address', 'services')

    inlines = [
        LinkInline,
    ]

class LinkAdmin(admin.ModelAdmin):
    list_display = ('expert', 'label', 'url')
    list_filter = ('expert', 'label')
    search_fields = ('expert', 'url')
