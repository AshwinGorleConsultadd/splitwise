from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
# Create your views here.
def index(request):
    return HttpResponse("Hello, world! This is the index view of the poll app.")

def get_question(request, question_id):
    return HttpResponse(f"You're looking at question {question_id}.")

def get_questions(request):
    question_list = Question.objects.all().order_by('-pub_date')
    template = loader.get_template('poll/index.html')
    context = {
        'latest_question_list': question_list
    }
    return HttpResponse(template.render(context,request))
    