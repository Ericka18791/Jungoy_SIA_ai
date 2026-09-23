from django.urls import path
from django.contrib import admin 
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('StudyResource_list', views.StudyResource_list, name='StudyResource_list'),
]