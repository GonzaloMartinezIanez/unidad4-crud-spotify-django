from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import User
from .serializer import UserSerializer
from rest_framework.response import Response
from .spotify import get_artists, get_songs

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(detail=True, methods=['get'])
    def artists(self, request, username=None):
        user = self.get_object()
        artists = get_artists(user.artists)
        
        return Response({
            "username": user.username,
            "artists": artists
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"])
    def songs(self, request, username=None):
        user = self.get_object()
        songs = get_songs(user.songs)
        
        return Response({
            "username": user.username,
            "songs": songs
        }, status=status.HTTP_200_OK)