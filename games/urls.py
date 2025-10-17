from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
