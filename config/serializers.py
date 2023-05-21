from django.contrib.auth import get_user_model
from .models import Hotel, Rating, Comment, Like, Amenities, Booking, HotelImages
from rest_framework import serializers
from django.db.models import Avg

User = get_user_model()

class HotelSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Hotel
        fields = '__all__'

    def validate_hotel_name(self, name):
        if self.Meta.model.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                'Отель с таким названием уже существует'
            )
        return name
    
    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['author'] = user
        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(Comment.objects.filter(hotel=instance.pk),many=True).data
        representation['likes_count'] = instance.likes.count()
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        representation['image'] = HotelImagesSerializer(instance.image.all(), many=True,context=self.context).data
        representation['booking'] = BookingSerializer(Booking.objects.filter(hotel=instance.pk),many=True).data
        representation['author'] = instance.author.email
        return representation
    
class HotelImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImages
        fields = '__all__'

    def get_image_url(self,obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self.get_image_url(instance)
        return representation
    

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment
    

class Likeserializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
    

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class Amenitiesserializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'


class RatingSerilizer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, rating):
        if not rating in range(1,6):
            raise serializers.ValidationError("Введите число от 1 до 5")
        return rating

    def create(self, validated_data):
        user = self.context.get('request').user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating


    def update(self,instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)