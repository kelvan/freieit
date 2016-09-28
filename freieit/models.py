from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField

from .choices import LABELS, COUNTRIES, CURRENCIES


class AuditedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ManyToManyField('self', blank=True, related_name='children')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ExpertProfile(AuditedModel):
    # the user this expert profile is associated with
    user = models.ForeignKey(User)

    # the experts name
    name = models.CharField(max_length=512)

    # experts image
    image = ThumbnailerImageField(
        upload_to='expert_images', verbose_name=_('image')
    )

    # the services this expert offers
    services = models.CharField(
        max_length=512, help_text=_('short description of the services'),
        verbose_name=_('services')
    )
    description = models.TextField(max_length=2048, blank=True, default='')

    # location of expert
    street = models.CharField(max_length=50, blank=True, default='')
    number = models.CharField(max_length=15, blank=True, default='')
    city = models.CharField(max_length=30)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=2, choices=COUNTRIES, default='AT')

    # time when the services can be offered
    time = models.CharField(
        max_length=1024, blank=True, default="",
        help_text=_('"opening hours"'), verbose_name=_("business times")
    )

    # charges for this expert
    charges = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=5,
        help_text=_('per hour incl. VAT, leave blank if variable'),
        verbose_name=_('charges')
    )
    currency = models.CharField(
        max_length=3, choices=CURRENCIES, blank=True, default="EUR",
        verbose_name=_("currency")
    )
    charges_details = models.CharField(
        blank=True, default='', max_length=512,
        help_text=_('eg traveling costs'), verbose_name=_('charge details')
    )

    # tags for this expert
    keywords = models.ManyToManyField(Tag, blank=True)

    references = models.TextField(
        blank=True, default="", help_text=_('Referenzkunden'),
        verbose_name=_('references')
    )
    available = models.BooleanField(
        default=False, help_text=_('disable eg if you are on holidays')
    )

    class Meta:
            # unique_together = (('user', 'name'),)
            verbose_name = _('Expert Profile')
            verbose_name_plural = _('Expert Profiles')
            ordering = ['name']

    def __str__(self):
        return self.name or self.user.get_full_name()

    @property
    def taglist(self):
        return ', '.join([t[1] for t in self.keywords.values_list()])

    @property
    def address(self):
        if self.street:
            return '%s %s, %s %s, %s' % (
                self.street, self.number,
                self.postcode, self.city, self.country
            )

    @property
    def price(self):
        if self.charges is None:
            return _('nach Vereinbarung')
        if self.charges == 0:
            return _('ehrenamtlich')
        return '%s %s' % (self.currency, self.charges)

    def get_absolute_url(self):
        return reverse('expert', kwargs={'pk': self.pk})


class Link(AuditedModel):
    expert = models.ForeignKey(ExpertProfile)
    label = models.CharField(max_length=20, choices=LABELS)
    url = models.CharField(max_length=200)
