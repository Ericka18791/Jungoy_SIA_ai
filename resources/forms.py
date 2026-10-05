from django import forms

from .models import StudyResource


class StudyResourceForm(forms.ModelForm):
    class Meta:
        model = StudyResource
        fields = [
            'title',
            'subject',
            'description',
            'resource_type',
            'author_uploader',
            'file',
            'external_link',
            'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the resource title'}),
            'subject': forms.TextInput(attrs={'placeholder': 'e.g. Biology, Literature, Algebra'}),
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Briefly describe what this resource contains...',
                }
            ),
            'author_uploader': forms.TextInput(
                attrs={'placeholder': 'Name of the author or person sharing this'}
            ),
            'external_link': forms.URLInput(
                attrs={'placeholder': 'https://example.com/resource'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        resource_file = cleaned_data.get('file')
        external_link = cleaned_data.get('external_link')

        if not resource_file and not external_link:
            raise forms.ValidationError(
                'Please provide either a file upload or an external link.'
            )

        return cleaned_data
