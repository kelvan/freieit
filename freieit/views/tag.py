from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator

from freieit.models import ExpertProfile

def show(request, tag, page_num=1):
  if not page_num:
    page_num=1
  expert_selection = ExpertProfile.objects.filter(keywords__tag=tag)

  experts_per_page = 1
  p = Paginator(expert_selection, experts_per_page)

  page={'current': int(page_num), 'last': p.num_pages}
  return render_to_response('experts.html',{'experts': p.page(page_num), 'tag': tag, 'page': page})
