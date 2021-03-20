from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Matrix(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наименование')
    tasks = models.ManyToManyField('Tasks', verbose_name='Задачи')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользоваетль', null=True)
    anon = models.BooleanField(default=True, verbose_name='Анон')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Матрица'
        verbose_name_plural = 'Матрицы'


class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользоваетль')
    task = models.CharField(max_length=300, verbose_name='Задача')

    def __str__(self):
        return f'Задача пользователя - {self.user.id}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
