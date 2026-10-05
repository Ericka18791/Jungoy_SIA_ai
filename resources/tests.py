from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import StudyResource


class StudyResourceViewTests(TestCase):
    def setUp(self):
        self.resource = StudyResource.objects.create(
            title='Algebra Notes',
            subject='Mathematics',
            description='Review notes for algebra topics.',
            resource_type=StudyResource.ResourceType.NOTES,
            author_uploader='Alice',
            external_link='https://example.com/algebra-notes',
            status=StudyResource.Status.ACTIVE,
        )

    def test_resource_list_page_loads(self):
        response = self.client.get(reverse('resource_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Algebra Notes')

    def test_resource_detail_and_form_pages_load(self):
        detail_response = self.client.get(reverse('resource_detail', args=[self.resource.pk]))
        create_response = self.client.get(reverse('resource_create'))
        update_response = self.client.get(reverse('resource_update', args=[self.resource.pk]))

        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'Algebra Notes')
        self.assertEqual(create_response.status_code, 200)
        self.assertEqual(update_response.status_code, 200)

    def test_home_page_renders_database_statistics(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'STUDYHUB')
        self.assertContains(response, 'Total resources')
        self.assertContains(response, 'Algebra Notes')

    def test_subject_detail_page_loads(self):
        response = self.client.get(reverse('subject_detail', args=['Mathematics']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Algebra Notes')

    def test_resource_filters_use_existing_resource_data(self):
        response = self.client.get(reverse('resource_list'), {'reviewer': 'Alice'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Algebra Notes')

        response = self.client.get(reverse('resource_list'), {'status': StudyResource.Status.ARCHIVED})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Algebra Notes')

    def test_create_resource_with_valid_data(self):
        response = self.client.post(
            reverse('resource_create'),
            {
                'title': 'Biology Review',
                'subject': 'Biology',
                'description': 'Summary of key biology chapters.',
                'resource_type': StudyResource.ResourceType.REVIEWER,
                'author_uploader': 'Bob',
                'external_link': 'https://example.com/biology-review',
                'status': StudyResource.Status.ACTIVE,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(StudyResource.objects.filter(title='Biology Review').exists())

    def test_update_resource_with_valid_data(self):
        response = self.client.post(
            reverse('resource_update', args=[self.resource.pk]),
            {
                'title': 'Updated Algebra Notes',
                'subject': 'Mathematics',
                'description': 'Updated review notes.',
                'resource_type': StudyResource.ResourceType.NOTES,
                'author_uploader': 'Alice',
                'external_link': 'https://example.com/algebra-notes',
                'status': StudyResource.Status.ACTIVE,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.resource.refresh_from_db()
        self.assertEqual(self.resource.title, 'Updated Algebra Notes')

    def test_delete_resource_requires_confirmation_then_deletes(self):
        response = self.client.get(reverse('resource_delete', args=[self.resource.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Remove this resource')

        response = self.client.post(reverse('resource_delete', args=[self.resource.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(StudyResource.objects.filter(pk=self.resource.pk).exists())

    def test_seed_resources_command(self):
        StudyResource.objects.all().delete()
        call_command('seed_resources')
        self.assertGreater(StudyResource.objects.count(), 0)
