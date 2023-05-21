from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Amenities(models.Model):
    amenity_name = models.CharField(max_length=100)

    def __str__(self):
        return self.amenity_name
    


class Hotel(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='hotel')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    amenities = models.ManyToManyField(Amenities,related_name='hotel',blank=True)
    room_count = models.IntegerField(default=5)
    country = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.name} in {self.country}'



class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='image')
    image = models.ImageField()



class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='likes')
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='likes')
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'Liked {self.hotel} by {self.author.name}'
    

class Booking(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='booking')
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='booking')
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Booked {self.hotel} by {self.author}'

    
class Rating(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ratings')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='ratings')
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.rating} -> {self.hotel}'
    


class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='comments')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.author.name} to {self.hotel.name}' 
    

