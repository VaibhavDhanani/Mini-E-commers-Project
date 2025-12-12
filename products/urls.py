from django.urls import path
from .views import ProductDetailAPIView, ProductListCreateAPIView

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view()),
    path('products/<int:id>/', ProductDetailAPIView.as_view()),
]