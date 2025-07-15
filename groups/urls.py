from django.urls import path, include
from .views import group_view

urlpatterns = [
   path('',group_view, name='group_view'),
]