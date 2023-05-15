from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно зарегестрирован', status=200)

