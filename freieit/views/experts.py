from django.http import HttpResponse
from django.shortcuts import render_to_response

from freieit.models import ExpertProfile

def show(request):

  state = {'experts': ExpertProfile.objects.all() }

  if request.user.is_authenticated():
    state.update( {'user': request.user} )

  return render_to_response('experts.html',state)
  #return render_to_response('base.html')


