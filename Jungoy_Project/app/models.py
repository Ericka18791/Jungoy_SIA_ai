from django.db import models


# Create your models here.

class StudyResource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    resource_type = models.CharField(max_length=50)
    author_uploader = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    file_or_link = models.CharField(max_length=500)
    status = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.title