import json
import requests
import logging
from google.cloud import storage
from stats.models import ActivityOccurence
from rest_framework.decorators import api_view
from vertexai.generative_models import GenerativeModel
from wordcloud import WordCloud
from vertexai import init
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import ExtractMinute
from django.utils import timezone
from io import BytesIO
from datetime import timedelta

# Create your views here.

BUCKET_NAME = "panduanmemori-cdn"
PROJECT_ID = "panduanmemori"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.0-flash-001"
init(project=PROJECT_ID, location=LOCATION)

logger = logging.getLogger(__name__)

storage_client = storage.Client()
model = GenerativeModel(MODEL_NAME)
duration_expr = ExpressionWrapper(F('end_time') - F('actual_start_time'), output_field=DurationField())

def upload_to_gcs(file_content, destination_blob_name, bucket_name):
    """Uploads a file to Google Cloud Storage and returns the GCS URL."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        if isinstance(file_content, str):
            # If file_content is a local path
            blob.upload_from_filename(file_content)
        else:
            # If file_content is file data
            blob.upload_from_string(file_content)
        gcs_uri = f"gs://{bucket_name}/{destination_blob_name}"
        logger.info(f"Successfully uploaded file to {gcs_uri}")
        return gcs_uri
    except Exception as e:
        logger.error(f"Error uploading to GCS: {str(e)}")
        raise


def get_patient_schedule(patient_id):
    return ActivityOccurence.objects.filter(activity__patient_id=patient_id)

def get_percentage(activity_occurence_list):
    all_count_activities = activity_occurence_list.count()
    if all_count_activities == 0:
        return {'tepat_waktu': 0, 'telat': 0, 'terlewat': 0}
    logger.info(all_count_activities)
    count_tepat_waktu = activity_occurence_list.filter(is_on_time=True).count()
    count_complete_activities = activity_occurence_list.filter(is_completed=True).count()
    return {
        'tepat_waktu': (count_tepat_waktu / all_count_activities) * 100,
        'telat': (count_complete_activities - count_tepat_waktu) / all_count_activities * 100,
        'terlewat': (all_count_activities - count_complete_activities) / all_count_activities * 100
    }

def get_kesesuaian_jadwal(list_activities):
    categories = ['makan', 'tidur', 'obat']
    results = {}
    try:
        results['semua'] = get_percentage(list_activities)
        for cat in categories:
            filtered_activity = list_activities.filter(activity__activity_category__name=cat)
            logger.info(filtered_activity)
            results[cat] = get_percentage(filtered_activity)
    except Exception as e:
        logger.error(f"Error in get_kesesuaian_jadwal: {e}", exc_info=True)
        raise
    return results

@api_view(['GET'])
def get_kesesuaian_jadwal_all(request):
    try:
        last_month = timezone.now() - timedelta(days=30)
        all_activities = ActivityOccurence.objects.filter(actual_start_time__gte=last_month)
        data = get_kesesuaian_jadwal(all_activities)
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in get_kesesuaian_jadwal_all: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_kesesuaian_jadwal_pasien(request, patient_id):
    try:
        last_month = timezone.now() - timedelta(days=30)
        patient_activities = ActivityOccurence.objects.filter(
            actual_start_time__gte=last_month,
            activity__patient_id=patient_id
        )

        data = get_kesesuaian_jadwal(patient_activities)
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in get_kesesuaian_jadwal_pasien: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_avg_duration(list_activities):
    try:
        categories = ['makan', 'tidur']
        results = {}
        for cat in categories:
            filtered_activities = list_activities.filter(activity__activity_category__name=cat)
            filtered_activities = filtered_activities.annotate(duration=duration_expr)
            avg_duration = filtered_activities.aggregate(avg_minutes=Avg(ExtractMinute('duration')))['avg_minutes']
            results[cat] = avg_duration
        return results
    except Exception as e:
        logger.error(f"Error in get_kesesuaian_jadwal_pasien: {e}", exc_info=True)
        return {}
    
@api_view(['GET'])
def get_durasi_all(request):
    try:
        last_month = timezone.now() - timedelta(days=30)
        all_activities = ActivityOccurence.objects.filter(actual_start_time__gte=last_month)
        return Response(get_avg_duration(all_activities), status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in get_durasi_all: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_durasi_pasien(request, patient_id):
    try:
        last_month = timezone.now() - timedelta(days=30)
        patient_activities = ActivityOccurence.objects.filter(actual_start_time__gte=last_month, activity__patient_id=patient_id)#sebulan terakhir)
        return Response(get_avg_duration(patient_activities), status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in get_durasi_pasien: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_patient_summary(request, patient_id):
    try:
        url = f'https://storage.googleapis.com/panduanmemori-cdn/conversations/{patient_id}.json'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        string_content = ' '.join(entry['content'] for entry in data if 'content' in entry)
        summary = get_summary_from_vertex_ai(data)
        patient_id = str(patient_id)
        word_cloud_path = get_word_cloud(patient_id, string_content)
        response = {'summary': summary, 'gcs_word_cloud_path': word_cloud_path}
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in get_patient_summary: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_summary_from_vertex_ai(logs):
    """ Send logs to Vertex AI's Gemini 2.0 Flash and get summary. """
    response = model.generate_content(
        "Berikut ini adalah log aktivitas percakapan seorang pasien demensia dengan AI assistant selama satu minggu. "
        "Rangkum log berikut menjadi satu paragraf yang mudah dibaca:\n"
        + json.dumps(logs, indent=2),
        generation_config={"temperature": 0.2, "max_output_tokens": 256}
    )
    return response.text.strip()


def get_word_cloud(patient_id, string_content):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(string_content)
    
    img_buffer = BytesIO()
    wordcloud.to_image().save(img_buffer, format='PNG')
    img_buffer.seek(0)

    word_cloud_blob_path = f"word_clouds/{patient_id}.png"
    return upload_to_gcs(img_buffer.getvalue(), word_cloud_blob_path, BUCKET_NAME)