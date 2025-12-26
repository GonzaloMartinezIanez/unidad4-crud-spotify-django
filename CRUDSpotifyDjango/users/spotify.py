from django.conf import settings
import requests
from django.core.cache import cache

# Funcion que devuelve el token de la cache o genera otro y lo devuelve
def get_spotify_token():
    token = cache.get('SPOTIFY_TOKEN')

    # Esta el token en la cache o todavia no ha expirado
    if token:
        return "Bearer " + token["access_token"]

    endpoint_access = "https://accounts.spotify.com/api/token"
    header_data = {
        "grant_type": "client_credentials",
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET
    }

    get_token = requests.post(endpoint_access, headers={"Content-Type": "application/x-www-form-urlencoded"}, data=header_data).json()

    # Se guarda en la cache el token y el tiempo de expiracion menos un minuto para que no se haga una llamada con el token expirado
    cache.set("SPOTIFY_TOKEN", { "access_token": get_token["access_token"] }, timeout=get_token["expires_in"] - 60)

    return "Bearer " + get_token["access_token"]

# Funcion que devuelve una lista con los artistas y sus datos mas importantes
def get_artists(ids):
    artists_ids = ",".join(ids)

    endpoint = f"https://api.spotify.com/v1/artists?ids={artists_ids}"
    response = requests.get(endpoint, headers={"Authorization": get_spotify_token()})

    # Se ha producido un error, lo mas probable es que los ids estan mal
    if response.status_code != 200:
        return None
    
    # Crear un objeto en foramto json con la informacion
    all_data = response.json()["artists"]
    formated_data = []
    for data in all_data:
        formated_data.append(
            {
                "name": data["name"],
                "id": data["id"],
                "followers": data["followers"]["total"],
                "popularity": data["popularity"],
                "genres": data["genres"],
                "url": data["external_urls"]["spotify"]
            })
        
    return formated_data

def get_songs(ids):
    songs_ids = ",".join(ids)

    endpoint = f"https://api.spotify.com/v1/tracks?ids={songs_ids}"
    response = requests.get(endpoint, headers={"Authorization": get_spotify_token()})

    if response.status_code != 200:
        return None

    all_data = response.json()["tracks"]
    formated_data = []
    for data in all_data:
        if data is not None:
            formated_data.append(
                {
                    "name": data["name"],
                    "id": data["id"],
                    "duration_ms": data["duration_ms"],
                    "popularity": data["popularity"],
                    "url": data["external_urls"]["spotify"],
                    "album": {
                        "album_type": data["album"]["album_type"],
                        "total_tracks": data["album"]["total_tracks"],
                        "id": data["album"]["id"],
                        "release_data": data["album"]["release_date"],
                        "name": data["album"]["name"],
                        "url": data["album"]["external_urls"]["spotify"]
                    },
                    "artist": {
                        "name": data["artists"][0]["name"],
                        "id": data["artists"][0]["id"],
                        "url": data["artists"][0]["external_urls"]["spotify"]
                    }
                })
        
    return formated_data
