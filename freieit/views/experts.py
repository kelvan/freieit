from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator

from freieit.models import ExpertProfile

def show(request, page_num=1):

  expert_selection = ExpertProfile.objects.all()

  experts_per_page = 1
  p = Paginator(expert_selection, experts_per_page)

  page={'current': int(page_num), 'last': p.num_pages}
  return render_to_response('experts.html',{'experts': p.page(page_num), 'page': page})
  #return render_to_response('base.html')


