from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from audited_models.models import AuditedModel
from choices import LABELS, COUNTRIES, CURRENCIES

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ManyToManyField('self', null=True, blank=True,
                                    related_name='children')

    def __unicode__(self):
        return self.name

class ExpertProfile(AuditedModel):
    # the user this expert profile is associated with
    user = models.ForeignKey(User)

    # the experts name
    name = models.CharField(max_length=512)

    # experts image
    image = models.ImageField(upload_to="expert_images",
                              verbose_name = _('image'))

    # the services this expert offers
    services = models.CharField(max_length=512,
                                help_text=_("short description of the services"),
                                verbose_name = _('services'))
    description = models.TextField(max_length=2048, blank=True, default="")

    # location of expert
    street = models.CharField(max_length=50, blank=True, default="")
    number = models.CharField(max_length=15, blank=True, default="")
    city = models.CharField(max_length=30)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=2, choices=COUNTRIES, default="AT")

    # time when the services can be offered
    time = models.CharField(max_length=1024, blank=True, default="",
                            help_text=_('"opening hours"'),
                            verbose_name=_("business times"))

    # charges for this expert
    charges = models.DecimalField(null=True,
                                  default=None,
                                  blank=True,
                                  decimal_places=2,
                                  max_digits=5,
                                  help_text=_('per hour incl. VAT, leave blank if variable'),
                                  verbose_name=_("charges"))
    currency = models.CharField(max_length=3, choices=CURRENCIES,
                                blank=True, default="EUR",
                                verbose_name=_("currency"))
    charges_details = models.CharField(blank=True, default="",
                                       max_length=512,
                                       help_text=_("eg traveling costs"),
                                       verbose_name=_("charge details"))

    # tags for this expert
    keywords = models.ManyToManyField(Tag, null=True, blank=True)

    references = models.TextField(blank=True, default="",
                                  help_text=_("Referenzkunden"),
                                  verbose_name=_("references"))
    available = models.BooleanField(default=True, help_text=_("disable eg if you are on holidays"))

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
    def taglist(self):
        return ", ".join(map(lambda t: t[1], self.keywords.values_list()))

    @property
    def address(self):
        if self.street:
            return "%s %s, %s %s, %s" % (self.street, self.number,
                                         self.postcode, self.city, self.country)

    @property
    def price(self):
        if self.charges == None:
            return _("nach Vereinbarung")
        if self.charges == 0:
            return _("ehrenamtlich")
        return "%s %s" % (self.currency, self.charges)

    def get_absolute_url(self):
        return "/expert/%s" % self.user.username

class Link(AuditedModel):
    expert = models.ForeignKey(ExpertProfile)
    label = models.CharField(max_length=20, choices=LABELS)
    url = models.CharField(max_length=200)



class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['parent__name']

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
