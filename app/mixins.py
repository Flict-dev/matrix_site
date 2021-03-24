from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import View

from app.models import Matrix


class MatrixMixin(View):
    titles = (
        'Важно - Срочно',
        'Важно - Не срочно',
        'Не важно - Срочно',
        'Не важно - Не срочно',
    )

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            mat = Matrix.objects.filter(user=request.user).select_related('user')
            if len(mat) == 0:
                for title in self.titles:
                    Matrix.objects.create(user=request.user, title=title, anon=False)
                mat = Matrix.objects.filter(user=request.user).select_related('user')
        else:
            mat = Matrix.objects.filter(anon=True)
        self.matrices = mat
        return super().dispatch(request, *args, **kwargs)
