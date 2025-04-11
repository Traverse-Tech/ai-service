import uuid
from django.db import models

class ActivityCategory(models.Model):
    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'ActivityCategory' 

class Activity(models.Model):
    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    patient_id = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'Activity' 

class ActivityOccurence(models.Model):
    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    recurrence_id = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField()
    is_completed = models.BooleanField()
    is_deleted = models.BooleanField()
    is_on_time = models.BooleanField()
    actual_start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        db_table = 'ActivityOccurence' 