from django.db import models


class StudyResource(models.Model):
    class ResourceType(models.TextChoices):
        REVIEWER = "Reviewer", "Reviewer"
        NOTES = "Notes", "Notes"
        LEARNING_MATERIAL = "Learning Material", "Learning Material"
        STUDY_GUIDE = "Study Guide", "Study Guide"

    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        ARCHIVED = "Archived", "Archived"

    resource_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    resource_type = models.CharField(
        max_length=30,
        choices=ResourceType.choices,
        default=ResourceType.NOTES,
    )
    author_uploader = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to="resources/files/", blank=True, null=True)
    external_link = models.URLField(max_length=500, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        verbose_name = "Study Resource"
        verbose_name_plural = "Study Resources"

    def __str__(self):
        return self.title