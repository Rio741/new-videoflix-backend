from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import uuid

User = get_user_model()

class UserTests(APITestCase):
    
    def test_registration(self):
        url = reverse('registration')
        data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'confirmedPassword': 'password123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Registrierung erfolgreich! Bitte bestätige deine E-Mail.')
        
        user = User.objects.get(email=data['email'])
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.verification_token)
        
    def test_login_success(self):
        user = User.objects.create_user(email='testuser@example.com', password='password123')
        user.is_active = True
        user.save()

        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        
    def test_login_inactive_user(self):
        user = User.objects.create_user(email='testuser@example.com', password='password123')
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }

        user.is_active = False
        user.save()

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Bitte bestätige zuerst deine E-Mail.')


    def test_verify_email(self):
        user = User.objects.create_user(email='testuser@example.com', password='password123')
        token = user.verification_token
        url = reverse('verify-email', args=[token])

        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'E-Mail erfolgreich bestätigt! Du kannst dich jetzt einloggen.')
        
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        
    def test_verify_email_already_verified(self):
        user = User.objects.create_user(email='testuser@example.com', password='password123')
        user.is_active = True
        user.save()

        token = user.verification_token
        url = reverse('verify-email', args=[token])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Dein Konto wurde bereits aktiviert.')

        
    def test_password_reset_request(self):
        user = User.objects.create_user(email='testuser@example.com', password='password123')
        url = reverse('password-reset')
        data = {'email': 'testuser@example.com'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Falls die E-Mail existiert, wurde eine Nachricht gesendet.')

        user.refresh_from_db()
        self.assertIsNotNone(user.verification_token)

    def test_password_reset_confirm(self):
        user = User.objects.create_user(email='testuser@example.com', password='password123')
        reset_token = str(uuid.uuid4())
        user.verification_token = reset_token
        user.save()

        url = reverse('password-reset-confirm')
        data = {
            'token': reset_token,
            'password': 'newpassword123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Passwort erfolgreich zurückgesetzt! Du kannst dich jetzt einloggen.')

        user.refresh_from_db()
        self.assertTrue(user.check_password('newpassword123'))
        
    def test_resend_confirmation_email(self):
        user = User.objects.create_user(email='testuser@example.com', password='password123')
        url = reverse('resend-confirmation-email')
        data = {'email': 'testuser@example.com'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Eine Bestätigungs-E-Mail wurde erneut gesendet.')

        user.refresh_from_db()
        self.assertIsNotNone(user.verification_token)
