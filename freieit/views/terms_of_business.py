from django.http import HttpResponse
from django.shortcuts import render_to_response


def show(request):
  return render_to_response('terms_of_business.html')


