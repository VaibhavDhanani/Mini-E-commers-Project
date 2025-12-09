from django.urls import path
from .views import orders, order, order_items, order_item

urlpatterns = [
    path('orders/', orders),
    path('orders/<int:id>/', order),
    path('order-items/',order_items),
    path('order-items/<int:id>/',order_item),
]