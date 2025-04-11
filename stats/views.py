from stats.models import ActivityOccurrence

# Create your views here.

def get_patient_schedule(patient_id):
    return ActivityOccurrence.objects.filter(activity__patient_id=patient_id)

def define_time(activity_occurence_list):
    counter = len(activity_occurence_list)
    tepat_waktu_activities = activity_occurence_list.filter(activity__is_on_time=True)
    act = activity_occurence_list.filter(activity__is_completed=True)

def get_kesesuaian_jadwal_all():
    # get semua activity occurence pada sebulan terakhir
    all_activities = ActivityOccurrence.objects.filter(activity__created_at='')#sebulan terakhir)
    categories = ['makan', 'tidur', 'obat']
    results = {}
    for cat in categories:
        filtered_activity = all_activities.filter(activity__category=cat)
        


    pass

def get_kesesuaian_jadwal_pasien(patient_id):
    pass

def get_durasi_all():
    pass

def get_durasi_pasien(patient_id):
    pass

def get_word_cloud(patient_id):
    pass