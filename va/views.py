from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VARequest
from .serializers import VARequestSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from .storage import upload_to_gcs

# Create your views here.
@api_view(['GET'])
def index(request):
  return Response({'message': 'Hello, world!'})

@api_view(['POST'])
def va_request(request):
  serializer = VARequestSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO: implement voice assistant flow
# 1. receive audio file and save it to the Google Cloud Storage Bucket (GCS) and return the path
# 2. send the path to the speech-to-text API and get the text
# 3. send the text to vertex AI's LLM API and get the answer
# 4. send the answer to the text-to-speech API and store the audio file to the GCS and return the path
# 5. return the audio file path

@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_file(request):
    """Handles file upload to Google Cloud Storage."""
    if "file" not in request.FILES:
        return Response({"error": "No file provided"}, status=400)

    file = request.FILES["file"]
    file_url = upload_to_gcs(file, file.name)

    return Response({"file_url": file_url}, status=201)
