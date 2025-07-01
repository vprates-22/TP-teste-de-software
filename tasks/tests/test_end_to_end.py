from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task, Tag

class EndToEndTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_full_user_signup_and_login_flow(self):
        # Usuário se cadastra
        response = self.client.post(reverse('tasks:signup'), {
            'username': 'e2euser',
            'password1': 'SuperSenha123',
            'password2': 'SuperSenha123',
        })
        self.assertRedirects(response, reverse('tasks:login'))

        # Usuário faz login
        response = self.client.post(reverse('tasks:login'), {
            'username': 'e2euser',
            'password': 'SuperSenha123',
        })
        self.assertRedirects(response, reverse('tasks:task_list'))

    def test_user_creates_task_with_tag_and_priority(self):
        user = User.objects.create_user(username='e2euser', password='senha123')
        self.client.login(username='e2euser', password='senha123')
        tag = Tag.objects.create(name='Projeto', user=user)

        # Criação de uma tarefa com prioridade e tag
        response = self.client.post(reverse('tasks:task_create'), {
            'title': 'Finalizar relatório',
            'description': 'Até sexta',
            'priority': '1',
            'tags': [tag.name],
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.first()

        self.assertEqual(task.title, 'Finalizar relatório')
        self.assertEqual(task.priority, '1')
        self.assertIn(tag, task.tags.all())

    def test_task_appears_in_list(self):
        user = User.objects.create_user(username='e2euser', password='senha123')
        self.client.login(username='e2euser', password='senha123')
        Task.objects.create(title='Ver tarefa', user=user)
        response = self.client.get(reverse('tasks:task_list'))
        self.assertContains(response, 'Ver tarefa')

    def test_user_completes_task(self):
        user = User.objects.create_user(username='e2euser', password='senha123')
        self.client.login(username='e2euser', password='senha123')
        task = Task.objects.create(title='Tarefa 1', user=user)
        response = self.client.post(reverse('tasks:task_toggle', args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_user_filters_task_by_tag(self):
        user = User.objects.create_user(username='e2euser', password='senha123')
        self.client.login(username='e2euser', password='senha123')
        tag1 = Tag.objects.create(name='Trabalho', user=user)
        tag2 = Tag.objects.create(name='Pessoal', user=user)

        task1 = Task.objects.create(title='Reunião', user=user)
        task1.tags.add(tag1)

        task2 = Task.objects.create(title='Academia', user=user)
        task2.tags.add(tag2)

        response = self.client.get(reverse('tasks:task_list') + '?tag=Trabalho')
        self.assertContains(response, 'Reunião')
        self.assertNotContains(response, 'Academia')
