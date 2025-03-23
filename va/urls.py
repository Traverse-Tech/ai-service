from django.urls import path
from .views import VoiceAssistantView
from va import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('test/', views.index),
    path('upload/', views.upload_file),
    path("/", VoiceAssistantView.as_view(), name="voice_assistant"),
]

urlpatterns = format_suffix_patterns(urlpatterns)