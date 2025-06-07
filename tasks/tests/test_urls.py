from django.test import SimpleTestCase
from django.urls import reverse, resolve
from tasks import views

class TestUrls(SimpleTestCase):
    def test_landing_url_resolves(self):
        url = reverse('tasks:landing')
        self.assertEqual(resolve(url).func, views.landing_page)

    def test_login_url_resolves(self):
        url = reverse('tasks:login')
        self.assertEqual(resolve(url).func, views.user_login)

    def test_signup_url_resolves(self):
        url = reverse('tasks:signup')
        self.assertEqual(resolve(url).func, views.user_signup)

    def test_task_list_url(self):
        url = reverse('tasks:task_list')
        self.assertEqual(resolve(url).func, views.task_list)