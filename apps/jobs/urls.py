from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.get_all_jobs, name='get_all_jobs'),
    path('jobs/<str:pk>/',views.get_by_id_job,name='get_by_id_job'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/update/<str:pk>/', views.update_job,name='update_job'),
    path('jobs/delete/<str:pk>/',views.delete_job,name='delete_job'),
]
