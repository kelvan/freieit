from django.http import HttpResponse
from django.shortcuts import render_to_response


def show(request):
  return render_to_response('tips_and_tricks.html')


