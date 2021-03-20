from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import View

from app.models import Matrix


class MatrixMixin(View):
    titles = ('Срочно', 'Не срочно', 'Важно', 'Не важно')

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
