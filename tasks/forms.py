from django import forms
from .models import Task, Tag

class TaskForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Separe as tags por vírgulas. Ex: estudo, urgente"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'tags']
