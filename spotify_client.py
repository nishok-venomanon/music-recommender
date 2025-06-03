import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your Spotify app credentials
SPOTIPY_CLIENT_ID = "62cb56241f1146f89ef7caf711da9d22"
SPOTIPY_CLIENT_SECRET = "f385714ae55f42ce8856702ee6809c20"
#SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback/"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback/"

def create_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-library-read user-read-recently-played user-top-read"
    ))

def get_recent_tracks(sp, limit=50):
    results = sp.current_user_recently_played(limit=limit)
    tracks = []
    for item in results["items"]:
        track = item["track"]
        tracks.append({
            "track": track["name"],
            "artist": track["artists"][0]["name"],
            "played_at": item["played_at"],
            "album": track["album"]["name"],
            "uri": track["uri"]
        })
    return tracks

def get_audio_features_for_tracks(sp, tracks):
    track_ids = list({t["uri"].split(":")[-1] for t in tracks})
    print(f"Fetching audio features for {len(track_ids)} unique tracks...")

    valid_ids = [tid for tid in track_ids if tid and len(tid) == 22]  # ✅ Spotify IDs are always 22 chars

    features = []
    for i in range(0, len(valid_ids), 50):
        batch = valid_ids[i:i+50]
        try:
            features += sp.audio_features(batch)
        except Exception as e:
            print(f"Failed on batch {i}: {e}")

    # Add features to tracks
    id_to_features = {f["id"]: f for f in features if f}
    for track in tracks:
        tid = track["uri"].split(":")[-1]
        if tid in id_to_features:
            f = id_to_features[tid]
            track["audio_features"] = {
                "danceability": f["danceability"],
                "energy": f["energy"],
                "tempo": f["tempo"],
                "valence": f["valence"]
            }

    return tracks
