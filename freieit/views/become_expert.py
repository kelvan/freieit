from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def show(request):

  state = {}

  if request.user.is_authenticated():
    state.update( {'user': request.user} )

  return render_to_response('become_expert.html',state)


