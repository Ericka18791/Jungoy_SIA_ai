from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subjects/<str:subject_name>/', views.subject_detail, name='subject_detail'),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/new/', views.resource_create, name='resource_create'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('resources/<int:pk>/edit/', views.resource_update, name='resource_update'),
    path('resources/<int:pk>/delete/', views.resource_delete, name='resource_delete'),
]