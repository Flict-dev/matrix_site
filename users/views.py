from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from users.forms import MyRegistrationForm, ProfileForm


class RegistrationView(View):
    def get(self, request):
        return render(request, 'users/registration.html', context={'form': MyRegistrationForm})

    def post(self, request, **kwargs):
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            return render(request, 'users/registration.html', context={'form': form})


class MyLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


@method_decorator(login_required, name='get')
class ProfileView(View):
    def get(self, request):
        return render(request, 'users/profile.html', context={
            'form': ProfileForm(instance=request.user)
        })

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.email = form.cleaned_data['email']
            user.save()
            messages.info(request, 'Почта обновлена')
            return redirect('/profile/')
        else:
            return render(request, 'users/profile.html', context={'form': form})
