from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsTests(APITestCase):
    def test_register_and_token(self):
        url = reverse('register')
        data = {
            "email":"player@test.com",
            "password":"StrongPass123!",
            "first_name":"Player",
            "recovery_question":"Pet name?",
            "recovery_answer":"Fido",
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        token_resp = self.client.post(reverse('token_obtain_pair'), {"email":"player@test.com","password":"StrongPass123!"})
        self.assertEqual(token_resp.status_code, 200)
        self.assertIn('access', token_resp.data)

    def test_recovery_reset(self):
        user = User.objects.create(email='r@test.com')
        user.set_password('OldPass123!')
        user.recovery_question = 'Q'
        user.set_recovery_answer('Answer')
        user.save()
        resp = self.client.post(reverse('recover_reset'), {"email":"r@test.com","answer":"Answer","new_password":"NewPass123!"})
        self.assertEqual(resp.status_code, 200)
        # try login with new password
        token_resp = self.client.post(reverse('token_obtain_pair'), {"email":"r@test.com","password":"NewPass123!"})
        self.assertEqual(token_resp.status_code, 200)
