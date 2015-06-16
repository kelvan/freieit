from django.shortcuts import render


def show(request):
    return render(request, 'register.html')


def invite(request):
    return render(request, 'invite.html')
