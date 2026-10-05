from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudyResourceForm
from .models import StudyResource


def home(request):
    latest_resources = StudyResource.objects.all().order_by('-date_added')[:5]
    subject_list = StudyResource.objects.order_by('subject').values_list('subject', flat=True).distinct()
    total_resources = StudyResource.objects.count()
    total_subjects = StudyResource.objects.order_by('subject').values_list('subject', flat=True).distinct().count()
    total_reviewers = StudyResource.objects.filter(resource_type=StudyResource.ResourceType.REVIEWER).count()

    context = {
        'latest_resources': latest_resources,
        'subject_list': subject_list,
        'total_resources': total_resources,
        'total_subjects': total_subjects,
        'total_reviewers': total_reviewers,
    }
    return render(request, 'resources/home.html', context)


def subject_detail(request, subject_name):
    resources = StudyResource.objects.filter(subject__iexact=subject_name).order_by('-date_added')
    return render(
        request,
        'resources/subject_detail.html',
        {'subject_name': subject_name, 'object_list': resources},
    )


def resource_list(request):
    queryset = StudyResource.objects.all()

    search = request.GET.get('search', '')
    subject = request.GET.get('subject', '')
    resource_type = request.GET.get('resource_type', '')
    reviewer = request.GET.get('reviewer', '')
    status = request.GET.get('status', '')

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(subject__icontains=search)
            | Q(description__icontains=search)
            | Q(author_uploader__icontains=search)
        )
    if subject:
        queryset = queryset.filter(subject__icontains=subject)
    if resource_type:
        queryset = queryset.filter(resource_type=resource_type)
    if reviewer:
        queryset = queryset.filter(author_uploader=reviewer)
    if status:
        queryset = queryset.filter(status=status)

    queryset = queryset.order_by('-date_added')
    reviewers = (
        StudyResource.objects.order_by('author_uploader')
        .values_list('author_uploader', flat=True)
        .distinct()
    )
    context = {
        'object_list': queryset,
        'search': search,
        'subject': subject,
        'resource_type': resource_type,
        'resource_type_choices': StudyResource.ResourceType.choices,
        'reviewer': reviewer,
        'reviewers': reviewers,
        'status': status,
        'status_choices': StudyResource.Status.choices,
    }
    return render(request, 'resources/resource_list.html', context)


def resource_detail(request, pk):
    resource = get_object_or_404(StudyResource, pk=pk)
    return render(request, 'resources/resource_detail.html', {'resource': resource})


def resource_create(request):
    if request.method == 'POST':
        form = StudyResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save()
            return redirect('resource_detail', pk=resource.pk)
    else:
        form = StudyResourceForm()

    return render(request, 'resources/resource_form.html', {'form': form, 'is_edit': False})


def resource_update(request, pk):
    resource = get_object_or_404(StudyResource, pk=pk)
    if request.method == 'POST':
        form = StudyResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource_detail', pk=resource.pk)
    else:
        form = StudyResourceForm(instance=resource)

    return render(request, 'resources/resource_form.html', {'form': form, 'resource': resource, 'is_edit': True})


def resource_delete(request, pk):
    resource = get_object_or_404(StudyResource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        return redirect('resource_list')

    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})
