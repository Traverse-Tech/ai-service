from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VARequest
from .serializers import VARequestSerializer

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