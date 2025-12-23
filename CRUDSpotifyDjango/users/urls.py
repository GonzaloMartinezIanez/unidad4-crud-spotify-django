from django.urls import path
from .views import UserListCreateView, UserDetailAPIView, UserArtistsAPIView, UserSongsAPIView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/artists/<str:username>/', UserArtistsAPIView.as_view(), name='user-list-artists'),
    path('users/songs/<str:username>/', UserSongsAPIView.as_view(), name='user-list-songs'),
    path('users/<str:username>/', UserDetailAPIView.as_view(), name='user-detail-by-username'),    
]