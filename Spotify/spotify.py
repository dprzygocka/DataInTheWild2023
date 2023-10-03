import json
import spotipy
import datetime
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import CLIENT_ID, CLIENT_SECRET


"""
Connection to Spotify API
"""
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
)

"""
Playlists for Polish Rap music
"""
rap_generacja = (
    "https://open.spotify.com/playlist/37i9dQZF1DWXJnyndhASBe?si=758917be953a4ebd"
)
polski_hip_hop_klasyki = (
    "https://open.spotify.com/playlist/37i9dQZF1DX6pGi5vfd9k8?si=a74e8cccf8ec49e7"
)
polski_rap_2000 = (
    "https://open.spotify.com/playlist/37i9dQZF1DX4tIiLXPvlZC?si=5a204cefe1ac45ab"
)
polski_rap_2010 = (
    "https://open.spotify.com/playlist/37i9dQZF1DX2htXmbzwcfL?si=8c8cb30c01f3448a"
)


def save_playlist_to_json(name: str, url: str) -> None:
    """
    Saves a playlist from a spotify url to a json file
    """
    results = spotify.playlist_items(url)
    date = datetime.datetime.now().strftime("%m-%d-%y")
    with open(f"playlists/{name}_{date}.json", "w") as f:
        json.dump(results, f, indent=4)


def name_artists_from_playlist(path_to_playlist_json: str) -> dict:
    """
    Returns a dictionary with song names and artists from a playlist json file
    """
    name_artists = []
    with open(path_to_playlist_json) as f:
        results = json.load(f)
    songs = results["items"]
    for song in songs:
        artists = [artist["name"] for artist in song["track"]["artists"]]
        name = song["track"]["name"]
        print(f"{name} - {artists}")
        name_artists.append({"name": name, "artists": artists})
    return {"items": name_artists}


def save_to_json(direcotry: str, name: str, content: dict) -> None:
    """
    Saves dictionary to a json file at given directory
    """
    date = datetime.datetime.now().strftime("%m-%d-%y")
    with open(f"{direcotry}/{name}_{date}.json", "w") as f:
        json.dump(content, f, indent=4)
