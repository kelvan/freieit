from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from freieit.forms.expert import ExpertProfileForm
from freieit.models import ExpertProfile
from django.http import Http404

def show(request):
    if request.user.is_anonymous():
        raise Http404

    e = get_object_or_404(ExpertProfile, user=request.user)
    
    if request.method == 'POST':
        form = ExpertProfileForm(request.POST, request.FILES, instance=e)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile')
    else:
        # check if logged in user has profile
        form = ExpertProfileForm(instance=e)

    return render_to_response('profile.html', RequestContext(request, {
        'form': form,
    }))
