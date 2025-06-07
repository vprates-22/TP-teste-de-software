from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Tag
from .forms import TaskForm

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='123')
        self.task = Task.objects.create(
            title='Test Task', description='Test Desc',
            priority='2', completed=False, user=self.user
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')

    def test_task_str(self):
        self.assertEqual(str(self.task), 'Test Task')

    def test_task_default_completed(self):
        self.assertFalse(self.task.completed)

    def test_task_priority(self):
        self.assertEqual(self.task.priority, '2')

    def test_task_user_link(self):
        self.assertEqual(self.task.user.username, 'user')


class TagModelTest(TestCase):
    def test_tag_creation(self):
        tag = Tag.objects.create(name='Urgente')
        self.assertEqual(str(tag), 'Urgente')


class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='123')
        self.client.login(username='user', password='123')
        self.task = Task.objects.create(
            title='Task View Test', description='View Test',
            priority='1', user=self.user
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task View Test')

    def test_task_create_view_get(self):
        response = self.client.get(reverse('tasks:task_create'))
        self.assertEqual(response.status_code, 200)

    def test_task_create_view_post(self):
        response = self.client.post(reverse('tasks:task_create'), {
            'title': 'New Task',
            'description': 'New Desc',
            'priority': '3',
        })
        self.assertEqual(Task.objects.count(), 2)

    def test_task_delete_view(self):
        response = self.client.post(reverse('tasks:task_delete', args=[self.task.id]))
        self.assertEqual(Task.objects.count(), 0)

    def test_task_toggle_view(self):
        response = self.client.post(reverse('tasks:task_toggle', args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)


class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='123')

    def test_landing_redirect_logged_in(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('tasks:landing'))
        self.assertRedirects(response, reverse('tasks:task_list'))

    def test_landing_view(self):
        response = self.client.get(reverse('tasks:landing'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view(self):
        response = self.client.post(reverse('tasks:signup'), {
            'username': 'newuser',
            'password1': 'Superpass123',
            'password2': 'Superpass123'
        })
        self.assertEqual(User.objects.count(), 2)

    def test_login_success(self):
        response = self.client.post(reverse('tasks:login'), {
            'username': 'user', 'password': '123'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('tasks:logout'))
        self.assertEqual(response.status_code, 302)


class TaskFormTest(TestCase):
    def test_valid_form(self):
        form = TaskForm(data={
            'title': 'Form Task',
            'description': 'Desc',
            'priority': '1'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = TaskForm(data={'title': ''})
        self.assertFalse(form.is_valid())

    def test_form_fields(self):
        form = TaskForm()
        self.assertIn('title', form.fields)
        self.assertIn('priority', form.fields)
        self.assertIn('tags', form.fields)


class TaskFilterAndOrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='filteruser', password='123')
        self.client.login(username='filteruser', password='123')
        tag1 = Tag.objects.create(name='work')
        tag2 = Tag.objects.create(name='home')

        self.task1 = Task.objects.create(title='Task A', priority='1', user=self.user)
        self.task2 = Task.objects.create(title='Task B', priority='2', completed=True, user=self.user)

        self.task1.tags.add(tag1)
        self.task2.tags.add(tag2)

    def test_filter_by_tag(self):
        response = self.client.get(reverse('tasks:task_list') + '?tag=work')
        self.assertContains(response, 'Task A')
        self.assertNotContains(response, 'Task B')

    def test_ordering_by_priority_and_completion(self):
        response = self.client.get(reverse('tasks:task_list'))
        tasks = list(response.context['tasks'])
        self.assertEqual(tasks[0].completed, False)
        self.assertEqual(tasks[0].priority, '1')


class AuthProtectionTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertRedirects(response, '/login/?next=/list/')
