from django.urls import path, include
from .views import UserListCreateView, UserDetailAPIView, UserArtistsAPIView, UserSongsAPIView
from .viewset import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'viewset', UserViewSet, basename='users-viewset')

urlpatterns = [
    path('api-view/', UserListCreateView.as_view(), name='user-list'),
    path('api-view/<str:username>/artists/', UserArtistsAPIView.as_view(), name='user-list-artists'),
    path('api-view/<str:username>/songs/', UserSongsAPIView.as_view(), name='user-list-songs'),
    path('api-view/<str:username>/', UserDetailAPIView.as_view(), name='user-detail-by-username'),
    path('', include(router.urls)),
]