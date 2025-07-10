from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='page'),
    path('<int:question_id>/',views.get_question, name='get_question'),
    path('questions/',views.get_questions, name='get_questions'),
]