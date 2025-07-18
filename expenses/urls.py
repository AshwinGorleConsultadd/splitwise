from django.urls import path, include
from .views import expense_view, expenses_view
urlpatterns = [
   path('',expenses_view, name='expenses_view'),
   path('<int:expense_id>/', expense_view, name='expense_delete'),
]