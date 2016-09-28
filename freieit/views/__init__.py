from django.shortcuts import render
from django.core.mail import send_mail
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.template import Context
from django.conf import settings

from ..models import ExpertProfile
from ..forms.expert import ExpertProfileForm, LinkFormSet


class ExpertView(DetailView):
    template_name='expert.html'
    model = ExpertProfile
    context_object_name = 'expert'


class NewExpertView(CreateView):
    template_name = 'newexpert.html'
    form_class = ExpertProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LinkFormSet(self.request.POST)
        else:
            context['formset'] = LinkFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            email = form.data['email']

            u, created = User.objects.get_or_create(email=email)
            if created:
                u.username = email
                u.set_unusable_password()
                u.save()

            expert = form.save(commit=False)
            expert.user = u
            expert.save()

            subject = "[New expert] %s" % expert.name
            email_msg = render_to_string('newexpert.txt', {'expert': expert})
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = settings.DEFAULT_FROM_EMAIL

            send_mail(
                subject, email_msg, email_from, [email_to], fail_silently=False
            )

            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return render(self.request, 'newexpert.html', {'expert': expert})
        else:
            return self.render_to_response(self.get_context_data(form=form))
