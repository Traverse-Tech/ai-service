from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from va import views

urlpatterns = [
    path('test/', views.index),
    path('/', views.va_request),
    path('upload/', views.upload_file),
]

urlpatterns = format_suffix_patterns(urlpatterns)