from django.urls import path, include
from .views import create_user, get_user, get_all_users

urlpatterns = [
    path('register/', create_user, name='register_user'),
    path('user/<int:user_id>/', get_user, name='get_user'),
    path('users/', get_all_users, name='get_all_users')
]