import grpc
from va import va_pb2
from va import va_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = va_pb2_grpc.VoiceAssistantServiceStub(channel)

with open("temp/test_audio.wav", "rb") as f:
    audio_bytes = f.read()

request = va_pb2.AudioRequest(
    session_id="test-session-123",
    audio_data=audio_bytes,
)

response = stub.ProcessAudio(request)

print("Session ID:", response.session_id)
print("Transcribed Text:", response.transcribed_text)
print("AI Response:", response.ai_response)
print("Audio Response URL:", response.audio_response_url)
