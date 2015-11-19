from django.shortcuts import render, get_object_or_404

from ..models import ExpertProfile


def show(request, expert):
    d = {'expert': get_object_or_404(ExpertProfile, user__username=expert)}
    return render(request, 'expert.html', d)
