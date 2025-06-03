import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="62cb56241f1146f89ef7caf711da9d22",
    client_secret="f385714ae55f42ce8856702ee6809c20",
    redirect_uri="http://127.0.0.1:8888/callback/",
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
