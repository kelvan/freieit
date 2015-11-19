from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings

from ..models import ExpertProfile


def show(request, page_num=1):
    d = {}
    experts_per_page = getattr(settings, 'EXPERTS_PER_PAGE', 5)

    if not page_num:
        page_num = 1

    expert_selection = ExpertProfile.objects.all()
    p = Paginator(expert_selection, experts_per_page)

    d['page'] = p.page(page_num)

    return render(request, 'experts.html', d)
