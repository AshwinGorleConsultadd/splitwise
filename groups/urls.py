from django.urls import path, include
from .views import groups_view, group_view

urlpatterns = [
   path('',groups_view, name='groups_view'),
   path('<int:group_id>/', group_view, name='group_view'),
]