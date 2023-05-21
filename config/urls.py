from django.urls import path, include
from .views import HotelViewSet, CommentViewSet, AmenitiesViewSet
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('hotels', HotelViewSet)
router.register('comments',CommentViewSet)
router.register('amenities', AmenitiesViewSet)



urlpatterns = [
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)