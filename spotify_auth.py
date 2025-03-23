import spotipy
from spotipy.oauth2 import SpotifyOAuth

#spotify API credentials
CLIENT_ID = "532883e4b1284629b6289ad1ec3ef4ce"
CLIENT_SECRET = "b62c1395829d428f8979ee46e1844fdb"
REDIRECT_URI = "http://127.0.0.1:8080/callback"

#authenticate and create a spotipy instance
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-currently-playing"
))


def get_current_song():
    #fetch the currently playing song from spotify
    track = sp.current_user_playing_track()
    if track is not None:
        song_name = track["item"]["name"]
        artist_name = track['item']['artists'][0]['name']
        album_cover_url = track['item']['album']['images'][0]['url']
        return song_name, artist_name, album_cover_url
    return None, None, None