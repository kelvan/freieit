from django.shortcuts import render

from .models import ExpertProfile


def show(request):
    return render(request, 'map.html')


def rss(request):
    experts = ExpertProfile.objects.all()
    d = {'experts': experts}
    return render(request, 'map.rss.xml', d)
