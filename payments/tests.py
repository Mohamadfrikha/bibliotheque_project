from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class PaymentsTests(TestCase):

    def test_success_page(self):
        response = self.client.get(reverse('payments:success'))
        self.assertEqual(response.status_code, 200)

    def test_cancel_page(self):
        response = self.client.get(reverse('payments:cancel'))
        self.assertEqual(response.status_code, 200)