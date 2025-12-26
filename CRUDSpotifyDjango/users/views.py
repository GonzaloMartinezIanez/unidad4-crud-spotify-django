from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from .spotify import get_artists, get_songs

# Funcion que usan multiples metodos para obtener un usuario o none si no hay
def get_user(username):
    try:
        return User.objects.get(username = username)
    except:
        return None


class UserListCreateView(APIView):
    # Metodo generico que devuelve todos los usuarios del sistema
    def get(self, request):
        users = User.objects.all()
        data = UserSerializer(users, many = True).data

        return Response(data, status = status.HTTP_200_OK)

    # Crea un solo usuario
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class UserDetailAPIView(APIView):
    # Obtener un usuario mediante su username    
    def get(self, request, username):
        user = get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(UserSerializer(user).data, status = status.HTTP_200_OK)
    
    # Modificar un usuario mediante su username
    # En el body se pueden mandar algunos de los atributos del usuario
    def put(self, request, username):
        user = get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data = request.data, partial = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    # Modificar un usuario mediante su username
    # Igual que put pero solo modifica un atributo del usuario
    def patch(self, request, username):
        user = get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    # Eliminar un usuario mediante su username
    def delete(self, request, username):
        user = get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)
    
class UserArtistsAPIView(APIView):
    # Haciendo uso de la api de spotify devuelve el usuario pasado como parametro
    # junto a un listado con los detalles de sus artistas
    def get(self, request, username):
        user = get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.artists is None:
            return Response({"message": "Este usuario no tiene artistas"}, status=status.HTTP_404_NOT_FOUND)
        
        artists = get_artists(user.artists)

        # Comprobar que los artistas son correctos
        if artists is None:
            return Response({"error": "Los artistas estan en un formato incorrecto"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(artists, status=status.HTTP_200_OK)
    
class UserSongsAPIView(APIView):
    # Igual que el de artistas pero para las canciones
    def get(self, request, username):
        user = get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.songs is None:
            return Response({"message": "Este usuario no tiene canciones"}, status=status.HTTP_404_NOT_FOUND)
        
        songs = get_songs(user.songs)

        # Comprobar que las canciones son correctas
        if songs is None:
            return Response({"error": "Las canciones estan en un formato incorrecto"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(songs, status=status.HTTP_200_OK)