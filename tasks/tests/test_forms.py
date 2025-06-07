from django.test import TestCase
from tasks.forms import TaskForm
from tasks.models import Tag

class TaskFormTest(TestCase):
    def test_form_valid(self):
        form_data = {'title': 'Nova tarefa', 'description': 'Descrição', 'priority': '2'}
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_title(self):
        form_data = {'description': 'Descrição', 'priority': '2'}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_priority_choices(self):
        form = TaskForm()
        self.assertIn(('1', 'Alta'), form.fields['priority'].choices)

    def test_tags_field_exists(self):
        form = TaskForm()
        self.assertIn('tags', form.fields)

    def test_form_invalid_priority(self):
        form_data = {'title': 'Tarefa', 'priority': '10'}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_empty_data(self):
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())