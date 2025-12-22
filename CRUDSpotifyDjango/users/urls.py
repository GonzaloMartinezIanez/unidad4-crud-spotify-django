from django.urls import path
from .views import UserListCreateView, UserDetailAPIView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<str:username>/', UserDetailAPIView.as_view(), name='user-detail-by-username'),    
]