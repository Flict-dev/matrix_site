from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic.base import View

from app.forms import TaskForm
from app.models import Matrix, Tasks


class MainView(View):
    titles = ('Срочно', 'Не срочно', 'Важно', 'Не важно')

    # Прописать одну модель матрицы
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                Matrix.objects.get(title=self.titles[0], user=request.user)
                mat = Matrix.objects.filter(user=request.user)
            except ObjectDoesNotExist:
                for title in self.titles:
                    Matrix.objects.create(user=request.user, title=title, anon=False)
                mat = Matrix.objects.filter(user=request.user)
        else:
            mat = Matrix.objects.filter(anon=True)
        self.matrices = mat
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        matrices = self.matrices
        form = TaskForm
        context = {
            'form': form,
            'matrices': matrices,
        }
        return render(request, 'main/index.html', context=context)

    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            form = TaskForm(request.POST)
            if form.is_valid():
                matrix = self.matrices.get(pk=kwargs.get('pk'))
                new_task = Tasks.objects.create(user=request.user, task=form.cleaned_data['task'])
                matrix.tasks.add(new_task)
                return redirect('/')
            else:
                return render(request, 'main/index.html', context={'form': form, 'matrices': self.matrices})
        else:
            messages.info(request, 'Для того чтобы начать заполнять матрицу зарегистрируйтесь')
            return redirect('/login/')
