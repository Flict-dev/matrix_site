from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic.base import View

from users.forms import MyRegistrationForm


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
