import openai
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.Client()
def embed_text(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding
def store_tracks_in_vector_db(tracks):
    collection = chroma_client.get_or_create_collection(name="songs")

    for i, t in enumerate(tracks):
        description = f"{t['track']} by {t['artist']} from the album '{t.get('album', '')}'"
        embedding = embed_text(description)
        collection.add(
            ids=[f"{i}-{t['track']}"],
            embeddings=[embedding],
            documents=[description]
        )
def find_similar_songs(query_text, top_k=5):
    embedding = embed_text(query_text)
    collection = chroma_client.get_collection("songs")
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    return results["documents"][0]
