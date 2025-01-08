from django.db import models

class UploadedFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('pdf', 'PDF'),
    ]
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file_path = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_path.name


class ImageMetadata(models.Model):
    file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE)
    width = models.IntegerField()
    height = models.IntegerField()
    channels = models.IntegerField()


class PDFMetadata(models.Model):
    file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE)
    num_pages = models.IntegerField()
    page_width = models.FloatField()
    page_height = models.FloatField()
