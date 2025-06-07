from django.test import TestCase, Client
from django.contrib.auth.models import User
from tasks.models import Task, Tag

class TagFilterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tagger', password='pass')
        self.client.login(username='tagger', password='pass')

    def test_tag_filtering_in_list_view(self):
        tag = Tag.objects.create(name='Filtrar', user=self.user)
        task = Task.objects.create(title='Filtrada', user=self.user)
        task.tags.add(tag)
        response = self.client.get('/list/?tag=Filtrar')
        self.assertContains(response, 'Filtrada')

    def test_tag_filter_no_match(self):
        Tag.objects.create(name='Outra', user=self.user)
        response = self.client.get('/list/?tag=Inexistente')
        self.assertNotContains(response, 'Inexistente')