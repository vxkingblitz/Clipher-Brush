from django.db import models

class ProcessingTask(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
    ]
    
    user_id = models.BigIntegerField()
    task_id = models.CharField(max_length=100, unique=True)
    original_image_path = models.CharField(max_length=500)
    input_colors = models.JSONField()
    output_bw_path = models.CharField(max_length=500, blank=True, null=True)
    output_color_path = models.CharField(max_length=500, blank=True, null=True)
    detected_colors = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'processing_tasks'
        ordering = ['-created_at']