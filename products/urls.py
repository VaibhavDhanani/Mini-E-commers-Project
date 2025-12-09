from django.urls import path
from .views import products, product

urlpatterns = [
    path('products/', products),
    path('products/<int:id>/', product),
]