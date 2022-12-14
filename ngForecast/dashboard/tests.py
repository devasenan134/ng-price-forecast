from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('dashboard:register')
        self.user = {
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "email": "test_email@gmail.com",
        }

        self.user_unmatching_passwd = {
            "username": "test_user",
            "password1": "test_password",
            "password2": "test",
            "email": "test_email@gmail.com",
        }

        self.user_short_passwd = {
            "username": "test_user",
            "password1": "tes",
            "password2": "tes",
            "email": "test_email@gmail.com",
        }

        self.user_invalid_email = {
            "username": "test_user",
            "password1": "test_passwd",
            "password2": "test_passwd",
            "email": "test_email.com",
        }

        return super().setUp()



class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/register.html")

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 302)

    def test_can_register_user_withunmatchingpasswords(self):
        response = self.client.post(self.register_url, self.user_unmatching_passwd, format="text/html")
        self.assertEqual(response.status_code, 200)

    def test_cant_register_user_withshortpassword(self):
        response = self.client.post(self.register_url, self.user_short_passwd, format="text/html")
        self.assertEqual(response.status_code, 200)

    def test_can_register_user_withtakenusername(self):
        self.client.post(self.register_url, self.user, format="text/html")
        response = self.client.post(self.register_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 200)
