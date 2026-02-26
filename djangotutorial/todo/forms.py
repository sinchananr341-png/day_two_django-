from django import forms
from .models import TodoItem


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'What needs to be done?',
                'autocomplete': 'off',
                'id': 'todo-input',
                'class': 'todo-input',
            }),
            'priority': forms.Select(attrs={
                'id': 'todo-priority',
                'class': 'todo-priority',
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'id': 'todo-due-date',
                'class': 'todo-due-date',
            }),
        }
