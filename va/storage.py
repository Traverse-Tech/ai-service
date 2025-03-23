from google.cloud import storage
from django.conf import settings

def upload_to_gcs(file, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(settings.GCP_QUESTION_BUCKET)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(file)
    blob.make_public()      # Make the file publicly accessible
    
    return blob.public_url  # Return the URL of the uploaded file
