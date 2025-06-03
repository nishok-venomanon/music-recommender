from spotify_client import create_spotify_client, get_recent_tracks, get_audio_features_for_tracks
from gpt_summarizer import summarize_tracks_with_gpt, recommend_similar_song
import openai
import json
import os
from embedder import store_tracks_in_vector_db, find_similar_songs
import chromadb
from chromadb.config import Settings

# Optional: load from .env instead of hardcoding
from dotenv import load_dotenv
load_dotenv()

# Step 1: Initialize clients
sp = create_spotify_client()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 2: Fetch & enrich tracks
tracks = get_recent_tracks(sp)
tracks = get_audio_features_for_tracks(sp, tracks)
store_tracks_in_vector_db(tracks)

# Step 3: Save to file
os.makedirs("data", exist_ok=True)
with open("data/enriched_tracks.json", "w") as f:
    json.dump(tracks, f, indent=2)

# Step 4: GPT summary
track_list_text = "\n".join([f"{t['track']} by {t['artist']}" for t in tracks])
summary = summarize_tracks_with_gpt(track_list_text, openai_client)
print("🎧 Weekly Summary:\n", summary)

# Step 5: Recommend songs like X
print("\n🎵 Recommendations similar to 'After Dark by Mr. Kitty':\n")
print(recommend_similar_song("After Dark by Mr. Kitty", openai_client))




import streamlit as st
from spotify_client import create_spotify_client, get_recent_tracks
from gpt_summarizer import summarize_tracks_with_gpt, recommend_similar_song
import openai
import json
import os
from datetime import datetime

# Init
st.set_page_config(page_title="🎧 Music Recapper", layout="centered")
st.title("🎧 What Did I Listen To?")
st.markdown("Your weekly music recap + smart recommendations")

# Setup API clients
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sp = create_spotify_client()

# Fetch data
if st.button("🔁 Get my recent tracks"):
    with st.spinner("Fetching your Spotify history..."):
        tracks = get_recent_tracks(sp)
        os.makedirs("data", exist_ok=True)
        with open("data/recent_tracks.json", "w") as f:
            json.dump(tracks, f, indent=2)

        track_list_text = "\n".join([f"{t['track']} by {t['artist']}" for t in tracks])
        summary = summarize_tracks_with_gpt(track_list_text, client)

        # Save summary for music diary
        week_key = datetime.now().strftime("%Y-%W")
        diary_file = "data/music_diary.json"
        diary = {}
        if os.path.exists(diary_file):
            with open(diary_file) as f:
                diary = json.load(f)
        diary[week_key] = summary
        with open(diary_file, "w") as f:
            json.dump(diary, f, indent=2)

        st.subheader("📅 This Week's Recap")
        st.text(summary)

# Recs based on a specific song
st.subheader("🎵 Get Recommendations Like a Song")
song_input = st.text_input("Enter a song name (e.g., After Dark by Mr. Kitty):")
if st.button("🎯 Recommend similar songs"):
    if song_input:
        with st.spinner("Asking GPT..."):
            recs = recommend_similar_song(song_input, client)
            st.markdown("#### 🎧 Recommendations:")
            st.text(recs)


st.subheader("🧊 Embeddings-Based Song Search")
query = st.text_input("Type a vibe like 'dreamy alt-pop' or a song: ")

if st.button("🔍 Find similar songs"):
    if query:
        similar = find_similar_songs(query)
        st.write("🎵 Similar songs:")
        for s in similar:
            st.markdown(f"- {s}")
