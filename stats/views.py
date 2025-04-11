from stats.models import ActivityOccurrence

# Create your views here.

def get_patient_schedule(patient_id):
    return ActivityOccurrence.objects.filter(activity__patient_id=patient_id)

def get_kesesuaian_jadwal_all():
    # get semua activity occurence pada sebulan terakhir
    ActivityOccurrence.objects.filter()
    
    pass

def get_kesesuaian_jadwal_pasien(patient_id):
    pass

def get_durasi_all():
    pass

def get_durasi_pasien(patient_id):
    pass

def get_word_cloud(patient_id):
    pass