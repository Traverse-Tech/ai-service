# utils/gcs_chat_history.py
from google.cloud import storage
import json

BUCKET_NAME = "panduanmemori-cdn"

def get_chat_history(user_id: str):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"conversations/{user_id}.json")
    
    if blob.exists():
        return json.loads(blob.download_as_text())
    return []

def save_chat_history(user_id: str, history: list):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"conversations/{user_id}.json")
    blob.upload_from_string(json.dumps(history), content_type="application/json")
