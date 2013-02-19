from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from freieit.forms.expert import ExpertProfileForm
from freieit import settings

def show(request):
    if request.method == 'POST':
        form = ExpertProfileForm(request.POST, request.FILES)
        if form.is_valid():
            email_msg = """
            Name:
            %(name)s

            Services:
            %(services)s
            """ % form.data

            subject = "[New expert] %s" % form.data['name']
            email_from = form.data['email']
            email_to = settings.DEFAULT_FROM_EMAIL

            email = EmailMessage(subject, email_msg, email_from, [email_to])

            if 'image' in request.FILES:
                img = request.FILES['image']
                email.attach(img.name, img.read(), img.content_type)
                
            email.send(fail_silently=False)
            
            return HttpResponseRedirect('/')
    else:
        form = ExpertProfileForm()
        
    return render(request, 'newexpert.html', {'form':form})
