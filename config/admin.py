from django.contrib import admin
from .models import  Hotel, Rating, Comment, Like, Amenities, Booking, HotelImages

admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Amenities)
admin.site.register(Comment)
admin.site.register(Booking)
admin.site.register(HotelImages)

class RatingInline(admin.TabularInline):
    model = Rating

class BookingInline(admin.TabularInline):
    model = Booking

class HotelImagesInline(admin.TabularInline):
    model = HotelImages

class CommentInline(admin.TabularInline):
    model = Comment

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'description', 'get_rating', 'get_likes')
    search_fields = ['name', 'country']
    inlines = (RatingInline,BookingInline,HotelImagesInline,CommentInline)
    list_filter = ['name','amenities']

    def get_rating(self, obj):
        from django.db.models import Avg
        result = obj.ratings.aggregate(Avg('rating'))
        return result['rating__avg']

    def get_likes(self, obj):
        a = obj.likes.count()
        return a 
    
admin.site.register(Hotel,HotelAdmin)
