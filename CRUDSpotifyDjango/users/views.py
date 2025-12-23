from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from .spotify import get_artists, get_songs

class UserListCreateView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = UserSerializer(users, many = True).data

        return Response(data, status = status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class UserDetailAPIView(APIView):
    def get_user(self, username):
        try:
            return User.objects.get(username = username)
        except:
            return None
        
    def get(self, request, username):
        user = self.get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(UserSerializer(user).data, status = status.HTTP_200_OK)
    
    def put(self, request, username):
        user = self.get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data = request.data, partial = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, username):
        user = self.get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, username):
        user = self.get_user(username)
        if not user:
            return Response({'error': f'User with username={username} not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)
    
class UserArtistsAPIView(APIView):
    def get(self, request, username):
        user = User.objects.get(username=username)
        artists = get_artists(user.artists)
        
        return Response(artists, status=status.HTTP_200_OK)
    
class UserSongsAPIView(APIView):
    def get(self, request, username):
        user = User.objects.get(username=username)
        songs = get_songs(user.songs)
        
        return Response(songs, status=status.HTTP_200_OK)