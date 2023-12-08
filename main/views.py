from django.shortcuts import render, redirect
from .forms import RegistrationForm, AuthForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


def index(request):
    return render(request, 'main/index.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('idx')
    form = RegistrationForm()
    return render(request, 'main/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('idx')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    form = AuthForm()
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('idx')
