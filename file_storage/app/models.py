from django.db import models

class StoredFile(models.Model):
    FILE_ORIGINAL = 'original'
    FILE_BW = 'bw'
    FILE_COLOR = 'color'
    
    FILE_TYPES = [
        (FILE_ORIGINAL, 'Original'),
        (FILE_BW, 'Black and White'),
        (FILE_COLOR, 'Color'),
    ]
    
    file_id = models.CharField(max_length=100, unique=True)
    user_id = models.BigIntegerField()
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    original_filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'storage_files'
        indexes = [
            models.Index(fields=['user_id', 'upload_date']),
        ]