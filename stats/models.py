import uuid
from django.db import models

class ActivityCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    patient_id = models.UUIDField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class ActivityOccurrence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    recurrence_id = models.UUIDField(null=True, blank=True)
    datetime = models.DateTimeField()
    is_completed = models.BooleanField()
    is_ontime = models.BooleanField()
    actual_start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()