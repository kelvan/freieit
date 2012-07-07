from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from freieit import settings

from django.core.context_processors import csrf

def show(request):

  if 'username' in request.POST.keys() and 'password' in request.POST.keys():

    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user:
      if user.is_active:
        login(request,user)
        return render_to_response('login_success.html',{'user': user})
      else:
        content = csrf(request)
        content.update({'login_error': True})
        return render_to_response('login_form.html',content)
    else:
      content = csrf(request)
      content.update({'login_error': True})
      return render_to_response('login_form.html',content)

  content = csrf(request)
  content['INVITE_ONLY'] = settings.INVITE_MODE
  return render_to_response('login_form.html', content)

def do_logout(request):
  logout(request)
  return render_to_response('login_logout_success.html')
