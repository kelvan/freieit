from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from freieit.models import ExpertProfile

def show(request):

  return render_to_response('map.html', RequestContext(request))

def rss(request):

  experts = ExpertProfile.objects.all()
  return render_to_response('map.rss.xml', RequestContext(request,{'experts':experts}))
