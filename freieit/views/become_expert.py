from django.http import HttpResponse
from django.shortcuts import render_to_response


def show(request):

  state = {}

  if request.user.is_authenticated():
    state.update( {'user': request.user} )

  return render_to_response('become_expert.html',state)


