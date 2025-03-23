from django.db import models

# Create your models here.
class VARequest(models.Model):
  audio_path = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)

class VAResponse(models.Model):
  text = models.TextField()
  va_request = models.ForeignKey(VARequest, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
