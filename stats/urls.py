from django.urls import path
from stats import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('get-kesesuaian-jadwal/all', views.index),
    path('get-kesesuaian-jadwal/<int:patient_id>', views.index),
    path('get-duration/all', views.index),
    path('get-duration/<int:patient_id>', views.index),
    path('get-word-cloud/<int:patient_id>', views.index),
]

urlpatterns = format_suffix_patterns(urlpatterns)