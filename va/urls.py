from django.urls import path
from va import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('healthcheck/', views.index),
    path('', views.voice_assistant),
]

urlpatterns = format_suffix_patterns(urlpatterns)