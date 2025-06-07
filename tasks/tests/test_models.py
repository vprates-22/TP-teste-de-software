from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task, Tag

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.tag = Tag.objects.create(name='Urgente', user=self.user)

    def test_create_task(self):
        task = Task.objects.create(title='Test Task', user=self.user)
        self.assertEqual(str(task), 'Test Task')

    def test_task_with_tag(self):
        task = Task.objects.create(title='Com Tag', user=self.user)
        task.tags.add(self.tag)
        self.assertIn(self.tag, task.tags.all())

    def test_task_completed_default(self):
        task = Task.objects.create(title='Default False', user=self.user)
        self.assertFalse(task.completed)

    def test_task_priority(self):
        task = Task.objects.create(title='Alta prioridade', user=self.user, priority='1')
        self.assertEqual(task.priority, '1')

    def test_tag_str(self):
        self.assertEqual(str(self.tag), 'Urgente')

    def test_task_str_representation(self):
        task = Task.objects.create(title='Teste Str', user=self.user)
        self.assertEqual(str(task), 'Teste Str')

    def test_task_multiple_tags(self):
        tag2 = Tag.objects.create(name='Trabalho', user=self.user)
        task = Task.objects.create(title='MultiTag', user=self.user)
        task.tags.set([self.tag, tag2])
        self.assertEqual(task.tags.count(), 2)