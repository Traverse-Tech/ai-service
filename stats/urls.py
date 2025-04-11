from django.urls import path
from stats import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('get-kesesuaian-jadwal/all', views.get_kesesuaian_jadwal_all),
    path('get-kesesuaian-jadwal/<str:patient_id>', views.get_kesesuaian_jadwal_pasien),
    path('get-duration/all', views.get_durasi_all),
    path('get-duration/<str:patient_id>', views.get_durasi_pasien),
    path('get-patient-summary/<str:patient_id>', views.get_patient_summary),
]

urlpatterns = format_suffix_patterns(urlpatterns)