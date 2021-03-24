from django.urls import path

from app.views import (
    MainView,
    AddTask,
    MatrixView,
    DeleteTask,
    DeleteAllTasks,
    SendEmailView,
    AboutView,
)

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('matrix/', MatrixView.as_view(), name='matrix'),
    path('add-to-matrix/<int:pk>/', AddTask.as_view(), name='add-task'),
    path('delete-from-matrix/<int:pk>/', DeleteTask.as_view(), name='delete-task'),
    path('reset/<int:pk>/', DeleteAllTasks.as_view(), name='reset'),
    path('send/', SendEmailView.as_view(), name='send'),
    path('about/', AboutView.as_view(), name='about'),
]
