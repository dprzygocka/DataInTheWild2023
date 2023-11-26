import os
import json
import spotipy
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

"""
Playlists for Croatian Rap music
"""
this_is_tram_11 = (
    "https://open.spotify.com/playlist/37i9dQZF1DZ06evO4ecEOC?si=f9f19d3ff1de4475"
)
bolesna_braca = (
    "https://open.spotify.com/playlist/37i9dQZF1E4mRVwtHBO6wH?si=7b8aa1cf887f4841"
)
marin_ivanovic_stoka = (
    "https://open.spotify.com/playlist/37i9dQZF1E4whjB3IyUubA?si=555d49ce9e644af6"
)
kid_rada = (
    "https://open.spotify.com/playlist/37i9dQZF1E4xQZ3DjXINt5?si=447a5dfdec2c495d"
)


"""
Polish Rappers
"""
sokol = "5Kuxl5ZenCl9fYzmtin6ot"
pezet = "4z93wkjfGntA0XFqnv4wj7"
peja = "5IQZA1dxUd3Qv73mHNln59"
ostr = "52XMlxvCIzmiNkzSqEw3Uv"
kaz_balagane = "2GzZAv52VCMdVli7QzkteT"
zdechly_osa = "509dS4Q0EfUQuG7KvaSsiz"


def playlist(url: str) -> dict:
    """
    Returns a playlist dictionary given a spotify url
    """
    playlist = spotify.playlist_items(url)
    return playlist


def playlist_name(url: str) -> str:
    """
    Returns formatted playlist name given a spotify url
    """
    playlist = spotify.playlist(url)
    return playlist["name"].strip().lower().replace(" ", "_")


def playlist_songs(url: str) -> dict:
    """
    Returns a dictionary with song names and artists from a playlist json file
    """
    songs = spotify.playlist_items(url)
    name_artists = [
        {
            "name": song["track"]["name"],
            "artists": [artist["name"] for artist in song["track"]["artists"]],
        }
        for song in songs["items"]
    ]
    for line in name_artists:
        print(line)
    return {"items": name_artists}


def save_to_json(name: str, content: dict, directory: str) -> str:
    """
    Saves dictionary to a json file at given directory
    """
    name = name.strip().lower().replace(" ", "_")

    if not os.path.exists(directory):
        os.makedirs(directory)

    path = f"{directory}/{name}.json"
    with open(path, "w") as f:
        json.dump(content, f, indent=4)
    return path


def save_playlist(url: str) -> str:
    """
    Saves playlist from a given url to json files
    """
    path = save_to_json(
        name=playlist_name(url), content=playlist(url), directory="playlists"
    )
    return path


def artist_albums(artist_id: str) -> dict:
    """
    Returns a dictionary with album name and album id from a given artist id
    """
    albums = spotify.artist_albums(artist_id)
    return [
        {
            "name": album["name"],
            "id": album["id"],
            "release_date": album["release_date"],
        }
        for album in albums["items"]
        if album["album_type"] == "album"
    ]


def album_songs(album_id: str) -> list[dict]:
    """
    Returns a dictionary with song name and song id from a given album id
    """
    songs = spotify.album_tracks(album_id)
    name_artists = [
        {
            "name": song["name"],
            "artists": [artist["name"] for artist in song["artists"]],
        }
        for song in songs["items"]
    ]
    for line in name_artists:
        print(line)
    return name_artists


def artist_name(artist_id: str) -> str:
    """
    Returns formatted artist name from a given artist id
    """
    artist = spotify.artist(artist_id)
    return artist["name"].strip().lower().replace(" ", "_").capitalize()


def save_artist_albums(artist_id: str) -> None:
    """
    Saves all albums from a given artist id to json files
    """
    albums = artist_albums(artist_id)
    for album in albums:
        print(album["name"])
        save_to_json(
            name=f'{album["name"]}_{album["release_date"]}',
            content={"items": album_songs(album["id"])},
            directory=f"artists/{artist_name(artist_id)}",
        )


save_artist_albums(zdechly_osa)
