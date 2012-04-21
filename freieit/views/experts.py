from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator

from freieit.models import ExpertProfile

def show(request, page_num=1):

  state = {}

  if not page_num:
    page_num=1

  if request.user.is_authenticated():
    state.update( {'user': request.user} )

  experts_per_page = 1
  p = Paginator(ExpertProfile.objects.all(), experts_per_page)

  state.update({'page':{'current': int(page_num), 'last': p.num_pages}})
  state.update({'experts':p.page(page_num)})

  return render_to_response('experts.html',state)
  #return render_to_response('base.html')


