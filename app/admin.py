from django.contrib import admin

from .models import Matrix, Tasks


@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'anon')
    list_filter = ('user', 'anon')
    raw_id_fields = ('tasks',)


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task')
    list_filter = ('user',)
