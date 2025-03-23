import os
import uuid
import logging
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from google.cloud import storage, speech, texttospeech
from google.api_core.exceptions import GoogleAPIError
from vertexai.generative_models import GenerativeModel
import vertexai
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .serializers import AudioUploadSerializer

# Create your views here.
@api_view(['GET'])
def index(request):
  return Response({'message': 'Hello, world!'})

# Configure logging
logger = logging.getLogger(__name__)

# Google Cloud Config
QUESTION_BUCKET_NAME = "panduanmemori-va-questions"
ANSWER_BUCKET_NAME = "panduanmemori-va-answers"
PROJECT_ID = "panduanmemori"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.0-flash-001"

# Initialize Google Cloud Clients
storage_client = storage.Client()
speech_client = speech.SpeechClient()
text_to_speech_client = texttospeech.TextToSpeechClient()

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)


def upload_to_gcs(file_content, destination_blob_name, bucket_name):
    """Uploads a file to Google Cloud Storage and returns the GCS URL."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        if isinstance(file_content, str):
            # If file_content is a local path
            blob.upload_from_filename(file_content)
        else:
            # If file_content is file data
            blob.upload_from_string(file_content)
        gcs_uri = f"gs://{bucket_name}/{destination_blob_name}"
        logger.info(f"Successfully uploaded file to {gcs_uri}")
        return gcs_uri
    except Exception as e:
        logger.error(f"Error uploading to GCS: {str(e)}")
        raise


def transcribe_audio(gcs_uri):
    """Converts speech to text using Google Cloud Speech-to-Text."""
    try:
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="id-ID",
        )
        response = speech_client.recognize(config=config, audio=audio)
        if not response.results:
            logger.warning("No transcription results returned")
            return ""
        transcript = response.results[0].alternatives[0].transcript
        logger.info(f"Transcribed text: {transcript}")
        return transcript
    except Exception as e:
        logger.error(f"Speech-to-text API error: {str(e)}")
        raise


def get_llm_response(text):
    """Gets a response from Vertex AI's Gemini model."""
    try:
        model = GenerativeModel(MODEL_NAME)
        response = model.generate_content(text)
        if not response or not hasattr(response, 'text'):
            logger.warning("No valid response from LLM")
            return "Sorry, I couldn't process your request."
        logger.info(f"LLM response generated: {response.text[:100]}...")
        return response.text
    except Exception as e:
        logger.error(f"Error getting LLM response: {str(e)}")
        raise


def text_to_speech(text, output_filename):
    """Converts text to speech and saves it as an audio file."""
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="id-ID",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        response = text_to_speech_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
        logger.info(f"Text-to-speech audio saved to {output_filename}")
        return output_filename
    except Exception as e:
        logger.error(f"Text-to-speech API error: {str(e)}")
        raise


def cleanup_temp_files(file_paths):
    """Clean up temporary files."""
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                logger.info(f"Deleted temporary file: {path}")
        except Exception as e:
            logger.warning(f"Failed to delete temporary file {path}: {str(e)}")


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def voice_assistant(request):
    """
    Complete voice assistant flow:
    1. Receive audio file and upload to GCS question bucket
    2. Transcribe audio to text
    3. Get response from LLM
    4. Convert response to speech
    5. Upload speech file to GCS answer bucket
    6. Return results
    """
    try:
        # Validate request
        if "audio" not in request.FILES:
            return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = request.FILES["audio"]
        session_id = request.data.get("session_id", str(uuid.uuid4()))
        
        # Create file paths and track for cleanup
        temp_files = []
        os.makedirs("temp", exist_ok=True)
        
        input_filename = f"{session_id}_input.wav"
        output_filename = f"{session_id}_output.wav"
        temp_input_path = os.path.join("temp", input_filename)
        temp_output_path = os.path.join("temp", output_filename)
        
        # Add to cleanup list
        temp_files.append(temp_input_path)
        temp_files.append(temp_output_path)
        
        # Save audio file temporarily
        with open(temp_input_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
                
        # 1. Upload to GCS question bucket
        gcs_question_path = upload_to_gcs(
            temp_input_path, 
            input_filename, 
            QUESTION_BUCKET_NAME
        )
        
        # 2. Speech-to-Text
        transcribed_text = transcribe_audio(gcs_question_path)
        if not transcribed_text:
            return Response(
                {"error": "Could not transcribe audio"}, 
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # 3. Get LLM Response
        ai_response = get_llm_response(transcribed_text)
        
        # 4. Convert Response to Speech
        text_to_speech(ai_response, temp_output_path)
        
        # 5. Upload TTS response to GCS answer bucket
        gcs_answer_path = upload_to_gcs(
            temp_output_path, 
            output_filename, 
            ANSWER_BUCKET_NAME
        )
        
        # Return results
        response_data = {
            "session_id": session_id,
            "transcribed_text": transcribed_text,
            "ai_response": ai_response,
            "audio_response_url": gcs_answer_path,
        }
        
        # Cleanup temporary files
        cleanup_temp_files(temp_files)
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Voice assistant error: {str(e)}")
        return Response(
            {"error": f"Processing failed: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )