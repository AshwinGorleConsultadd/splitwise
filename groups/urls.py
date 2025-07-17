from django.urls import path, include
from .views import groups_view, group_view, join_group

urlpatterns = [
   path('',groups_view, name='groups_view'),
   path('<int:group_id>/', group_view, name='group_view'),
   path('join/<int:group_id>/<int:user_id>', join_group, name='join_group')
]