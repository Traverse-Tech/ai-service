from va import va_pb2
from va import va_pb2_grpc
import os
import uuid
import logging
from google.cloud import storage, speech, texttospeech
from vertexai.generative_models import GenerativeModel
import vertexai
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

QUESTION_BUCKET_NAME = os.environ.get("QUESTION_BUCKET_NAME")
ANSWER_BUCKET_NAME = os.environ.get("ANSWER_BUCKET_NAME")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION = os.environ.get("GCP_LOCATION")
MODEL_NAME = os.environ.get("MODEL_NAME")

storage_client = storage.Client()
speech_client = speech.SpeechClient()
text_to_speech_client = texttospeech.TextToSpeechClient()
vertexai.init(project=PROJECT_ID, location=LOCATION)
logger = logging.getLogger(__name__)

class VoiceAssistantServicer(va_pb2_grpc.VoiceAssistantServiceServicer):
    def HealthCheck(self, request, context):
        return va_pb2.HealthCheckResponse(message="Hello, world!")

    def ProcessAudio(self, request, context):
        session_id = request.session_id or str(uuid.uuid4())
        temp_files = []
        os.makedirs("temp", exist_ok=True)
        input_filename = f"{session_id}_input.wav"
        output_filename = f"{session_id}_output.wav"
        temp_input_path = os.path.join("temp", input_filename)
        temp_output_path = os.path.join("temp", output_filename)
        temp_files.append(temp_input_path)
        temp_files.append(temp_output_path)
        
        with open(temp_input_path, "wb") as f:
            f.write(request.audio_data)
        
        converted_audio_path = self.convert_audio(temp_input_path, temp_input_path)
        gcs_question_path = self.upload_to_gcs(converted_audio_path, input_filename, QUESTION_BUCKET_NAME)
        transcribed_text = self.transcribe_audio(gcs_question_path)
        ai_response = self.get_llm_response(transcribed_text)
        self.text_to_speech(ai_response, temp_output_path)
        gcs_answer_path = self.upload_to_gcs(temp_output_path, output_filename, ANSWER_BUCKET_NAME)
        
        self.cleanup_temp_files(temp_files)
        
        return va_pb2.AudioResponse(
            session_id=session_id,
            transcribed_text=transcribed_text,
            ai_response=ai_response,
            audio_response_url=gcs_answer_path,
        )
    
    def upload_to_gcs(self, file_content, destination_blob_name, bucket_name):
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


    def transcribe_audio(self, gcs_uri):
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


    def get_llm_response(self, text):
        """Gets a response from Vertex AI's Gemini model."""
        try:
            system_prompt = '''Ini adalah curhatan seorang pasien demensia. Pasien ini membutuhkan seorang teman bercerita untuk
yang menanggapi dan mendengarkan dengan baik. Berikanlah respons yang singkat saja, tetapi sesuai untuk memvalidasi perasaannya dan mendengarkan curhatannya. Ajaklah ia lebih banyak mengobrol:\n'''
            model = GenerativeModel(MODEL_NAME)
            response = model.generate_content(system_prompt + text)
            if not response or not hasattr(response, 'text'):
                logger.warning("No valid response from LLM")
                return "Sorry, I couldn't process your request."
            logger.info(f"LLM response generated: {response.text[:100]}...")
            return response.text
        except Exception as e:
            logger.error(f"Error getting LLM response: {str(e)}")
            raise


    def text_to_speech(self, text, output_filename):
        """Converts text to speech and saves it as an audio file."""
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="id-ID",
                name="id-ID-Chirp3-HD-Leda",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
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


    def cleanup_temp_files(self, file_paths):
        """Clean up temporary files."""
        for path in file_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
                    logger.info(f"Deleted temporary file: {path}")
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {path}: {str(e)}")


    def convert_audio(self, input_audio_path, output_audio_path):
        """Converts audio to 16-bit PCM WAV, mono, 16kHz."""
        try:
            audio = AudioSegment.from_file(input_audio_path)
            audio = audio.set_sample_width(2)  # 2 bytes = 16-bit
            audio = audio.set_frame_rate(16000)  # Standard ASR sample rate
            audio = audio.set_channels(1)  # Mono for speech recognition
            audio.export(output_audio_path, format="wav")  # Save as WAV
            return output_audio_path
        except Exception as e:
            logger.error(f"Error converting audio: {str(e)}")
            raise