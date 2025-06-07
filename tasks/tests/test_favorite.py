from django.test import TestCase, Client
from django.contrib.auth.models import User
from tasks.models import Task
from django.urls import reverse

class FavoriteTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass')
        self.client.login(username='tester', password='pass')
        self.task = Task.objects.create(title='Favorita', user=self.user)

    def test_default_favorite_false(self):
        self.assertFalse(self.task.is_favorite)

    def test_toggle_favorite_to_true(self):
        response = self.client.post(reverse('tasks:task_favorite', args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_favorite)

    def test_toggle_favorite_to_false(self):
        self.task.is_favorite = True
        self.task.save()
        response = self.client.post(reverse('tasks:task_favorite', args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_favorite)

    def test_favorite_button_displayed(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertContains(response, 'Favoritar')

    def test_order_favorites_first(self):
        Task.objects.create(title='Normal', user=self.user, is_favorite=False)
        Task.objects.create(title='Favorita', user=self.user, is_favorite=True)
        response = self.client.get(reverse('tasks:task_list'))
        content = response.content.decode()
        self.assertLess(content.find('Favorita'), content.find('Normal'))
