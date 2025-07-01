from django.test import TestCase, Client
from django.contrib.auth.models import User
from tasks.models import Task, Tag
from django.urls import reverse

class TaskIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_task_flow(self):
        response = self.client.post(reverse('tasks:task_create'), {
            'title': 'Nova tarefa',
            'priority': '2',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

    def test_view_task_list(self):
        Task.objects.create(title='Ver lista', user=self.user)
        response = self.client.get(reverse('tasks:task_list'))
        self.assertContains(response, 'Ver lista')

    def test_complete_task(self):
        task = Task.objects.create(title='Completar', user=self.user)
        response = self.client.post(reverse('tasks:task_toggle', args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_delete_task(self):
        task = Task.objects.create(title='Excluir', user=self.user)
        response = self.client.post(reverse('tasks:task_delete', args=[task.id]))
        self.assertEqual(Task.objects.count(), 0)

    def test_add_task_with_tags(self):
        tag = Tag.objects.create(name='Estudo', user=self.user)
        response = self.client.post(reverse('tasks:task_create'), {
            'title': 'Com Tag',
            'priority': '1',
            'tags': [tag.name]
        })
        task = Task.objects.first()
        self.assertIn(tag, task.tags.all())

    def test_filter_task_by_tag(self):
        tag = Tag.objects.create(name='Casa', user=self.user)
        task = Task.objects.create(title='Arrumar', user=self.user)
        task.tags.add(tag)
        response = self.client.get(reverse('tasks:task_list') + '?tag=Casa')
        self.assertContains(response, 'Arrumar')

    def test_favorite_task(self):
        task = Task.objects.create(title='Favorita', user=self.user)
        self.client.post(reverse('tasks:task_favorite', args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.is_favorite)

    def test_signup_redirects_to_login(self):
        self.client.logout()
        response = self.client.post(reverse('tasks:signup'), {
            'username': 'newuser',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        })
        self.assertRedirects(response, reverse('tasks:login'))

    def test_task_ordering(self):
        t1 = Task.objects.create(title='Alta', user=self.user, priority='1')
        t2 = Task.objects.create(title='Baixa', user=self.user, priority='3')
        response = self.client.get(reverse('tasks:task_list'))
        content = response.content.decode()
        self.assertLess(content.find('Alta'), content.find('Baixa'))
