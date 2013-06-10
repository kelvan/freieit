from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context

from freieit.forms.expert import ExpertProfileForm
from freieit import settings

def show(request):
    if request.method == 'POST':
        form = ExpertProfileForm(request.POST, request.FILES)

        if form.is_valid():
            email = form.data['email']

            u, created = User.objects.get_or_create(email=email)
            if created:
                u.username = email
                u.set_unusable_password()
                u.save()

            expert = form.save(commit=False)
            expert.available = False
            expert.user = u
            expert.save()

            tpl = get_template('newexpert.txt')
            email_msg = tpl.render(Context({'expert': expert}))

            subject = "[New expert] %s" % expert.name
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = settings.DEFAULT_FROM_EMAIL

            email = EmailMessage(subject, email_msg, email_from, [email_to])

            #if 'image' in request.FILES:
            #    img = request.FILES['image']
            #    email.attach(img.name, img.read(), img.content_type)
            
            email.send(fail_silently=False)

            return render(request, 'newexpert.html', {'expert': expert})
    else:
        form = ExpertProfileForm()
        
    return render(request, 'newexpert.html', {'form': form})
