from rest_framework import status
from rest_framework.test import APITestCase

default_user = {
            "username": "Juan",
            "email": "juan@example.com",
            "favourite_genre": "Rock",
            "artists": ["49bzE5vRBRIota4qeHtQM8"],
            "songs": ["2UREu1Y8CO4jXkbvqAtP7g", "4CbKVDZkYKdv69I4bCaKUq"]
        }

# Test basicos para todos los endpoints usando apiview
class UserAPIViewTestCase(APITestCase):    
    def test_user_creation_apiview(self):
        res = self.client.post('/users/api-view/', default_user, format = "json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_create_same_username_apiview(self):
        data = {
            "username": "Juan",
            "email": "juan@example.com",
        }
        self.client.post('/users/api-view/', data, format = "json")
        res = self.client.post('/users/api-view/', data, format = "json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_bad_request_apiview(self):
        data = {
            "username": "",
            "email": "Maria@example.com",
        }
        res = self.client.post('/users/api-view/', data, format = "json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
   
    def test_user_get_apiview(self):
        res = self.client.get('/users/api-view/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_get_username_apiview(self):
        self.client.post('/users/api-view/', default_user, format = "json")
        res = self.client.get('/users/api-view/Juan/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_put_apiview(self):
        put_user = {
            "username": "Fernando",
            "email": "fernando@example.com",
            "favourite_genre": "Pop"
        }
        self.client.post('/users/api-view/', default_user, format="json")
        res = self.client.put("/users/api-view/Juan/", put_user, format = "json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_patch_apiview(self):
        patch_user = {
            "favourite_genre": "Pop"
        }
        self.client.post('/users/api-view/', default_user, format="json")
        res = self.client.patch("/users/api-view/Juan/", patch_user, format = "json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_user_delete_apiview(self):
        self.client.post('/users/api-view/', default_user, format="json")
        res = self.client.delete("/users/api-view/Juan/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_artists_apiview(self):
        self.client.post('/users/api-view/', default_user, format="json")
        res = self.client.get("/users/api-view/Juan/artists/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_artists_apiview(self):
        self.client.post('/users/api-view/', default_user, format="json")
        res = self.client.get("/users/api-view/Juan/songs/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

# Igual que el anterior pero para viewset
class UserViewsetTestCase(APITestCase):    
    def test_user_creation_viewset(self):
        res = self.client.post('/users/viewset/', default_user, format = "json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_create_same_username_viewset(self):
        data = {
            "username": "Juan",
            "email": "juan@example.com",
        }
        self.client.post('/users/viewset/', data, format = "json")
        res = self.client.post('/users/viewset/', data, format = "json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_bad_request_viewset(self):
        data = {
            "username": "",
            "email": "Maria@example.com",
        }
        res = self.client.post('/users/viewset/', data, format = "json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
   
    def test_user_get_viewset(self):
        res = self.client.get('/users/viewset/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_get_username_viewset(self):
        self.client.post('/users/viewset/', default_user, format = "json")
        res = self.client.get('/users/viewset/Juan/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_put_viewset(self):
        put_user = {
            "username": "Fernando",
            "email": "fernando@example.com",
            "favourite_genre": "Pop"
        }
        self.client.post('/users/viewset/', default_user, format="json")
        res = self.client.put("/users/viewset/Juan/", put_user, format = "json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_patch_viewset(self):
        patch_user = {
            "favourite_genre": "Pop"
        }
        self.client.post('/users/viewset/', default_user, format="json")
        res = self.client.patch("/users/viewset/Juan/", patch_user, format = "json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_user_delete_viewset(self):
        self.client.post('/users/viewset/', default_user, format="json")
        res = self.client.delete("/users/viewset/Juan/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_artists_viewset(self):
        self.client.post('/users/viewset/', default_user, format="json")
        res = self.client.get("/users/viewset/Juan/artists/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_artists_viewset(self):
        self.client.post('/users/viewset/', default_user, format="json")
        res = self.client.get("/users/viewset/Juan/songs/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)