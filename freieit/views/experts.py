from django.http import HttpResponse
from django.shortcuts import render_to_response

from freieit.models import ExpertProfile

def show(request):

  expert_selection = ExpertProfile.objects.all()

  return render_to_response('experts.html',{'experts': expert_selection})
  #return render_to_response('base.html')


