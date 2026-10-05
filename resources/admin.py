from django.contrib import admin

from .models import StudyResource


@admin.register(StudyResource)
class StudyResourceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'subject',
        'resource_type',
        'author_uploader',
        'date_added',
        'status',
    )
    list_filter = ('subject', 'resource_type', 'status')
    search_fields = ('title', 'subject', 'description', 'author_uploader')
    ordering = ('-date_added',)
