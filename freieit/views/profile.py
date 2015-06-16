from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms.expert import ExpertProfileForm
from .models import ExpertProfile


@login_required
def show(request):
    e = get_object_or_404(ExpertProfile, user=request.user)

    if request.method == 'POST':
        form = ExpertProfileForm(request.POST, request.FILES, instance=e)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile')
    else:
        # check if logged in user has profile
        form = ExpertProfileForm(instance=e)

    return render(request, 'profile.html', {'form': form})
