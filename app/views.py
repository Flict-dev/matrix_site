from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateView
from app.forms import TaskForm
from app.mixins import MatrixMixin
from app.models import Matrix, Tasks
from django.core.mail import send_mail
from Martix.settings import DEFAULT_FROM_EMAIL


class MainView(TemplateView):
    template_name = 'main/index.html'


class AboutView(TemplateView):
    template_name = 'main/about.html'


class MatrixView(MatrixMixin, View):
    def get(self, request):
        matrices = self.matrices
        form = TaskForm
        context = {
            'form': form,
            'matrices': matrices,
        }
        return render(request, 'main/matrix.html', context=context)


class AddTask(MatrixMixin, View):
    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            form = TaskForm(request.POST)
            if form.is_valid():
                matrix = self.matrices.get(pk=kwargs.get('pk'))
                matrix.tasks.add(Tasks.objects.create(
                    user=request.user,
                    task=form.cleaned_data['task']
                ))
                return redirect('/matrix/')
            else:
                return render(request, 'main/index.html', context={
                    'form': form,
                    'matrices': self.matrices
                })
        else:
            messages.info(request, 'Для того, чтобы начать редактировать матрицу зарегистрируйтесь')
            return redirect('/login/')


class DeleteTask(View):
    def get(self, request, **kwargs):
        Tasks.objects.filter(pk=kwargs.get('pk')).first().delete()
        return redirect('/matrix/')


class DeleteAllTasks(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            try:
                mat = Matrix.objects.get(pk=kwargs.get('pk'))
            except ObjectDoesNotExist:
                raise Http404
            mat.tasks.all().delete()
            return redirect('/matrix/')
        else:
            messages.info(request, 'Для того, чтобы начать редактировать матрицу зарегистрируйтесь')
            return redirect('/login/')


class SendEmailView(View):
    SUBJECT = 'Твоя Матрица'
    CONTENT = ''

    def get(self, request):
        if request.user.is_authenticated:
            matrices = Matrix.objects.filter(user=request.user)
            for matrix in matrices:
                tasks = ''
                count = 1
                for task in matrix.tasks.all():
                    tasks += str(count) + '.' + task.task + ' '
                    count += 1
                self.CONTENT = self.CONTENT + matrix.title + ': ' + tasks + '\n'
            mail = send_mail(
                self.SUBJECT,
                self.CONTENT,
                DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
            if mail:
                messages.info(request, 'Письмо отправлено. \n Осталось подождать!')
                return redirect('/profile/')
            messages.error(request, 'Ошибка отправки. \n Проверьте вашу почту!')
            return redirect('/profile/')
        messages.info(request, 'Зарегистрируйтесь, чтобы отправить данные на почту!')
        return redirect('/login/')