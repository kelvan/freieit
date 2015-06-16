from django.contrib import admin
from .models import Tag, Link, ExpertProfile


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['parent__name']


class LinkInline(admin.TabularInline):
    model = Link


@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'address', 'price')
    list_filter = ('country', 'city', 'keywords__name')
    search_fields = ('name', 'address', 'services')

    inlines = [
        LinkInline,
    ]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('expert', 'label', 'url')
    list_filter = ('expert', 'label')
    search_fields = ('expert', 'url')
