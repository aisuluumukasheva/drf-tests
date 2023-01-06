from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterAPIView
from .models import User


# setUp метод прогоняет код 

class AuthTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.create_user(
            email='test@gmail.com',
            password='12345678'
        )

    def test_register(self):
        data = {
            'email': 'new_user@gmail.com',
            'password': '12345678',
            'password_confirm': '12345678'
        }
    
        request = self.factory.post('/account/register/', data, format='json')
        view = RegisterAPIView.as_view()
        response = view(request)
        # print(response)
        
        assert response.status_code == 201
        assert User.objects.filter(email=data['email']).exists()
        # print(User.objects.all())

    def test_login(self):
        data = {
            'email': 'test@gmail.com',
            'password': '12345678',
        }
        request = self.factory.post('/account/token/', data, format='json')
        view = TokenObtainPairView.as_view()
        response = view(request)

        # print(response)
        assert response.status_code == 200
        # print(response.data)
        assert 'access' in response.data
        assert 'refresh' in response.data

