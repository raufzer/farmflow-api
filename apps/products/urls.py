from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_all_products, name='get_all_products'),
    path('products/<str:pk>/',views.get_by_id_product,name='get_by_id_product'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/update/<str:pk>/', views.update_product,name='update_product'),
    path('products/delete/<str:pk>/',views.delete_product,name='delete_product'),
]
