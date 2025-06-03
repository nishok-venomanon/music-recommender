def summarize_tracks_with_gpt(track_list_text, client):
    prompt = f"""Here is a list of songs I listened to this week:

{track_list_text}

Please summarize:
1. The overall mood and genre of my week
2. My favorite artists
3. Any pattern or vibe you notice
4. Suggest 3 songs I might like next
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def recommend_similar_song(song_name, client):
    prompt = f"""I like the song "{song_name}". Recommend 5 songs that are similar in mood, genre, or vibe."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
