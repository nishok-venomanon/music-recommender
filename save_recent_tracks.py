import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import json
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
#SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback/"
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-read-recently-played"
))

results = sp.current_user_recently_played(limit=50)

parsed_tracks = []
for item in results["items"]:
    track = item["track"]
    parsed_tracks.append({
        "track": track["name"],
        "artist": track["artists"][0]["name"],
        "played_at": item["played_at"],
        "album": track["album"]["name"],
        "uri": track["uri"]
    })

with open("data/recent_tracks.json", "w") as f:
    json.dump(parsed_tracks, f, indent=2)

print("✅ Saved 50 tracks to data/recent_tracks.json")
