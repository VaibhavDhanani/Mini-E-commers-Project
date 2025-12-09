from django.urls import path
from .views import users, user

urlpatterns = [
    path('users/', users),
    path('users/<int:id>/', user),
]