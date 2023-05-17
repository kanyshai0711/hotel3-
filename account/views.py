from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsActivePermission
from .serializers import RegistrationSerializer,  LoginSerializer, ActivationSerializer,  ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordCompleteSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer( data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=201)


class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer( data=request.data)
        serializer.is_valid( raise_exception=True)
        serializer.activate()
        return Response( 'Аккаунт успешно активирован', status=200)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsActivePermission]
    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response( 'вы вышли со своего аккаунта')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer( data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Status: 200. пароль успешно обновлен')


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('Вам выслали сообщение для восстановления' )

 
 
class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer( data=request.data)
        if serializer.is_valid( raise_exception=True):
            serializer.set_new_password()
            return Response( 'Пароль успешно изменен' )







