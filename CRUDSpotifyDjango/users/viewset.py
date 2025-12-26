from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import User
from .serializer import UserSerializer
from rest_framework.response import Response
from .spotify import get_artists, get_songs
    
# Alternativa con viewset, todos los metodos hacen lo mismo que la version con apiview
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Campo por el que se filtra
    lookup_field = 'username'

    @action(detail=True, methods=['get'])
    def artists(self, request, username=None):
        user = self.get_object()
        if user.artists is None:
            return Response({"message": "Este usuario no tiene artistas"}, status=status.HTTP_404_NOT_FOUND)
        
        artists = get_artists(user.artists)

        # Comprobar que los artistas son correctos
        if artists is None:
            return Response({"error": "Los artistas estan en un formato incorrecto"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "username": user.username,
            "artists": artists
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"])
    def songs(self, request, username=None):
        user = self.get_object()

        if user.songs is None:
            return Response({"message": "Este usuario no tiene artistas"}, status=status.HTTP_404_NOT_FOUND)
        
        songs = get_songs(user.songs)

        # Comprobar que las canciones son correctas
        if songs is None:
            return Response({"error": "Las canciones estan en un formato incorrecto"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "username": user.username,
            "songs": songs
        }, status=status.HTTP_200_OK)