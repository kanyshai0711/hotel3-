from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .views import RegistrationView,   LoginView, ChangePasswordView,  ForgotPasswordView,  ForgotPasswordCompleteView, LogoutView
from .models import User


class UserTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='user@gmail.com',
            password='1234',
            is_active=True
        )

    def test_register(self):
        data = {
            'email': 'new_user@gmail.com',
            'password': '4567',
            'password_confirm': '4567',
            'name': 'test',
            'last_name': 'TEST'
        }
        request = self.factory.post(
            'register/', data, format='json')
        # print(request)
        view = RegistrationView.as_view()
        response = view(request)
        # print(response)

        assert response.status_code == 201
        assert User.objects.filter(
            email=data['email']).exists()


    def test_login(self):
        data = {
            'email': 'user@gmail.com',
            'password': '1234'
        }
        request = self.factory.post('login/', data, format='json')
        view = LoginView.as_view()
        response = view(request)
        # print(response.data)

        assert response.status_code == 200
        assert 'token' in response.data

    def test_change_password(self):
        data = {
            'old_password': '1234',
            'new_password': '4567',
            'new_password_confirm': '4567',
        }
        request = self.factory.post( 'change_password/', data=data, format='json', )
        force_authenticate(request, user=self.user)
        view = ChangePasswordView.as_view()
        response = view(request)
        # print(response.data)

        # assert data['new_password_confirm'] == data['new_password']
        assert response.status_code == 200

    def test_forgot_password(self):
        data = { 'email': 'user@gmail.com'}
        request = self.factory.post('forgot_password', data, format='json')
        view = ForgotPasswordView.as_view()
        response = view(request)
        print(response.data)

        assert response.status_code == 200

    def test_logout(self):
        request = self.factory.post(
            'logout/')
        force_authenticate(request, user=self.user)
        view = LogoutView.as_view()
        response = view(request)
        print(response.data)

        assert response.status_code == 200


