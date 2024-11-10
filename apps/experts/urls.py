from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('experts/', views.get_all_experts, name='get_all_experts'),
    path('experts/<str:pk>/',views.get_by_id_expert,name='get_by_id_expert'),
    path('experts/create/', views.create_expert, name='create_expert'),
    path('experts/update/<str:pk>/', views.update_expert,name='update_expert'),
    path('experts/delete/<str:pk>/',views.delete_expert,name='delete_expert'),
]
