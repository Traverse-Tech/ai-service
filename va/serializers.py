from rest_framework import serializers
from .models import VARequest, VAResponse

class VARequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = VARequest
    fields = '__all__'

class VAResponseSerializer(serializers.ModelSerializer):
  class Meta:
    model = VAResponse
    fields = '__all__'
