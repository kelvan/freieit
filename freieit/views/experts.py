from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator

from freieit.models import ExpertProfile

def show(request, page_num=1):
  #TODO move to config
  experts_per_page = 2
  
  if not page_num:
    page_num=1

  expert_selection = ExpertProfile.objects.all()
  p = Paginator(expert_selection, experts_per_page)

  return render_to_response('experts.html', context_instance=RequestContext(request, {'page': p.page(page_num)}))
