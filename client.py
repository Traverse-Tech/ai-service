import grpc
from va import va_pb2
from va import va_pb2_grpc

# Load the gRPC stub
channel = grpc.insecure_channel("localhost:50051")  # Change port if needed
stub = va_pb2_grpc.VoiceAssistantServiceStub(channel)

# Read an audio file as bytes
with open("test_audio.wav", "rb") as f:
    audio_bytes = f.read()

# Create the request
request = va_pb2.AudioRequest(
    session_id="test-session-123",
    audio_data=audio_bytes,
)

# Call the API
response = stub.ProcessAudio(request)

# Print the response
print("Session ID:", response.session_id)
print("Transcribed Text:", response.transcribed_text)
print("AI Response:", response.ai_response)
print("Audio Response URL:", response.audio_response_url)
