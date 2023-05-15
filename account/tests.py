from django.test import TestCase
from rest_framework.test import force_authenticate, APITestCase, APIRequestFactory
from .views import RegistrationView
from .models import User

class UserTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email = 'test@gmail.com',
            password = '12345',
            is_active = True
        )
        
    def test_register(self):
        data = {
            'email': 'aikokulmiralimova@gmail.com',
            'password': '123456',
            'password_confirm': '123456',
            'name': 'aikokul',
            'last_name': 'm'
        }
        request = self.factory.post('register/', data, format='json')
        view = RegistrationView.as_view()
        response = view(request)
        print(response)

        assert response.status_code == 200
