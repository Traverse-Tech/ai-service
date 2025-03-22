from django.urls import path
from logservice.views import summarize_logs

urlpatterns = [
    path("api/summarize/", summarize_logs),
]
