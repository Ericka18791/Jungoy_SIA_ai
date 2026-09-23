from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def StudyResource_list(request):
    StudyResource = StudyResource.objects.all()

    context = {
        'StudyResource' :  StudyResource
    }

    return render(request, 'Jungoy_app/dashboard.html', context)
