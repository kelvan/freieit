from django.http import HttpResponse



from django.shortcuts import render_to_response

import os
import os.path


def terms_of_business(request):
  return render_to_response('terms_of_business.html')


