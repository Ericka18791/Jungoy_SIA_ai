from django.core.management.base import BaseCommand

from resources.models import StudyResource


class Command(BaseCommand):
    help = 'Seed the database with sample study resources for different subjects.'

    def handle(self, *args, **options):
        sample_resources = [
            {
                'title': 'Algebra Essentials Review',
                'subject': 'Mathematics',
                'description': 'A review sheet covering linear equations, factoring, and function basics.',
                'resource_type': StudyResource.ResourceType.REVIEWER,
                'author_uploader': 'A. Cruz',
                'external_link': 'https://example.com/algebra-essentials',
                'status': StudyResource.Status.ACTIVE,
            },
            {
                'title': 'Biology Chapter Summary',
                'subject': 'Biology',
                'description': 'Quick summary of cell structure, genetics, and photosynthesis.',
                'resource_type': StudyResource.ResourceType.NOTES,
                'author_uploader': 'L. Santos',
                'external_link': 'https://example.com/biology-summary',
                'status': StudyResource.Status.ACTIVE,
            },
            {
                'title': 'Chemistry Lab Guide',
                'subject': 'Chemistry',
                'description': 'A practical lab guide for safety, measurement, and experiment planning.',
                'resource_type': StudyResource.ResourceType.STUDY_GUIDE,
                'author_uploader': 'R. Garcia',
                'external_link': 'https://example.com/chemistry-lab-guide',
                'status': StudyResource.Status.ACTIVE,
            },
            {
                'title': 'World History Timeline',
                'subject': 'History',
                'description': 'A timeline of major events and civilizations from early modern periods.',
                'resource_type': StudyResource.ResourceType.LEARNING_MATERIAL,
                'author_uploader': 'J. Ramos',
                'external_link': 'https://example.com/world-history-timeline',
                'status': StudyResource.Status.ACTIVE,
            },
            {
                'title': 'Literature Reading Notes',
                'subject': 'English',
                'description': 'Notes on themes, symbols, and key literary devices in common texts.',
                'resource_type': StudyResource.ResourceType.NOTES,
                'author_uploader': 'M. Tan',
                'external_link': 'https://example.com/literature-notes',
                'status': StudyResource.Status.ACTIVE,
            },
        ]

        created = 0
        for data in sample_resources:
            resource, was_created = StudyResource.objects.get_or_create(
                title=data['title'],
                defaults={
                    'subject': data['subject'],
                    'description': data['description'],
                    'resource_type': data['resource_type'],
                    'author_uploader': data['author_uploader'],
                    'external_link': data['external_link'],
                    'status': data['status'],
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created} sample resources.'))
