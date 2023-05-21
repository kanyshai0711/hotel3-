from rest_framework import viewsets
from .serializers import HotelSerializer, RatingSerilizer, CommentSerializer, Amenitiesserializer
from django.contrib.auth import get_user_model
from .models import Hotel, Rating, Comment, Like, Amenities, Booking, HotelImages
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .permissions import IsOwnerPermission, IsAdminOrActivePermission
from rest_framework.permissions import AllowAny

User = get_user_model()

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'country']
    ordering_fields = ['created_at', 'name']

    @action(methods=['POST', 'PATCH'], detail=True)
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['hotel'] = pk
        rating = Rating.objects.filter(hotel=pk, author=request.user).first()
        serializer = RatingSerilizer(data=data, context={'request':request})

        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response('Вы уже оставляли рэйтинг, используйте PATCH запрос')
            elif rating and request.method == 'PATCH':
                serializer.update(rating, serializer.validated_data)
                return Response(serializer.data, status=204)
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data, status=201)     

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        hotel = self.get_object()
        user = request.user 
        try:
            like=Like.objects.get(hotel=hotel, author=user)
            like.delete()
            message = 'disliked'
        except Like.DoesNotExist:
            like = Like.objects.create(hotel=hotel, author=user)
            like.save()
            message = 'liked'
        return Response('liked', status=201)
    
    @action(['POST'],detail=True)
    def book(self,request,pk=None):
        hotel = self.get_object()
        user = request.user
        try:
            book=Booking.objects.get(hotel=hotel,author=user)
            book.delete()
            message = 'вы убрали бронь'
        except Booking.DoesNotExist:
            book = Booking.objects.create(hotel=hotel,author=user)
            book.save()
            message = 'забронировано'
        return Response(status=201)

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes=[IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes=[IsAdminOrActivePermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes=[IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes=[IsAdminOrActivePermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
class AmenitiesViewSet(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = Amenitiesserializer






    