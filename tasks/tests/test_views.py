from django.test import TestCase, Client
from django.contrib.auth.models import User
from tasks.models import Task, Tag
from django.urls import reverse

class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_landing_page_redirects(self):
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)

    def test_task_create(self):
        response = self.client.post(reverse('tasks:task_create'), {
            'title': 'Nova tarefa',
            'priority': '1'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

    def test_task_delete(self):
        task = Task.objects.create(title='Tarefa', user=self.user)
        response = self.client.post(reverse('tasks:task_delete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_toggle_completion(self):
        task = Task.objects.create(title='Toggle', user=self.user)
        response = self.client.post(reverse('tasks:task_toggle', args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_task_update_view(self):
        task = Task.objects.create(title='Editar', user=self.user)
        response = self.client.post(reverse('tasks:task_edit', args=[task.id]), {
            'title': 'Atualizada',
            'priority': '2'
        })
        task.refresh_from_db()
        self.assertEqual(task.title, 'Atualizada')
        task = Task.objects.create(title='Tarefa', user=self.user)
        response = self.client.post(reverse('tasks:task_delete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)