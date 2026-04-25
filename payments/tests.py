from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from decouple import config
class PaymentsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="123456"
        )
        self.client.login(username=config('TEST_USERNAME'), password=config('TEST_PASSWORD'))
    def test_success_page(self):
        response = self.client.get(reverse('payments:success'))
        self.assertEqual(response.status_code, 200)

    def test_cancel_page(self):
        response = self.client.get(reverse('payments:cancel'))
        self.assertEqual(response.status_code, 200)