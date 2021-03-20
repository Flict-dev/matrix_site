from django.forms import ModelForm
from django import forms


class TaskForm(forms.Form):
    task = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control w-100',
                'placeholder': 'Задача',
            },
        )
    )

    class Meta:
        fields = ('task',)
        labels = {
            'task': ' '
        }
