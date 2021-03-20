from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateView

from app.forms import TaskForm
from app.mixins import MatrixMixin
from app.models import Matrix, Tasks


class MainView(TemplateView):
    template_name = 'main/index.html'


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
                new_task = Tasks.objects.create(user=request.user, task=form.cleaned_data['task'])
                matrix.tasks.add(new_task)
                return redirect('/matrix/')
            else:
                return render(request, 'main/index.html', context={'form': form, 'matrices': self.matrices})
        else:
            messages.info(request, 'Для того чтобы начать заполнять матрицу зарегистрируйтесь')
            return redirect('/login/')


class DeleteTask(View):
    def get(self, request, **kwargs):
        task = Tasks.objects.get(pk=kwargs.get('pk'))
        task.delete()
        return redirect('/matrix/')
