from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from freieit.models import ExpertProfile

def show(request, expert):
  e = get_object_or_404(ExpertProfile, user__username=expert)

  return render_to_response('expert.html', RequestContext(request, {'expert': e}))
