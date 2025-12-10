from django.urls import path
from .views import UserView

urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/<int:user_id>/', UserView.as_view()),
]