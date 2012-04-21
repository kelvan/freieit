from django.http import HttpResponse
from django.shortcuts import render_to_response

from freieit.models import ExpertProfile

def show(request, tag):
    expert_selection = ExpertProfile.objects.filter(keywords__tag=tag)

    return render_to_response('experts.html',{'experts': expert_selection, 'tag': tag})
