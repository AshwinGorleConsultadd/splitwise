from django.urls import path, include
from .views import expenses_view
urlpatterns = [
   path('',expenses_view, name='expenses_view'),
]