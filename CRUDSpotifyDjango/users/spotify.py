from django.conf import settings
import requests

def get_spotify_token():
    endpoint_access = "https://accounts.spotify.com/api/token"
    header_data = {
        "grant_type": "client_credentials",
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET
    }

    get_token = requests.post(endpoint_access, headers={"Content-Type": "application/x-www-form-urlencoded"}, data=header_data)
    return "Bearer " + get_token.json()['access_token']

def get_artists(ids):
    artists_ids = ",".join(ids)

    endpoint = f"https://api.spotify.com/v1/artists?ids={artists_ids}"
    response = requests.get(endpoint, headers={"Authorization": get_spotify_token()})

    if response.status_code != 200:
        return None
    
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
