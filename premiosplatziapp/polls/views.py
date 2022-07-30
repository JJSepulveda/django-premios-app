""" Polls views """
# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Models
from .models import Question

# Create your views here.
def index(request):
	latest_question_list = Question.objects.all()
	context = {
		'latest_question_list': latest_question_list
	}
	return render(
		request=request,
		template_name="polls/index.html",
		context=context
	)


def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	context = {
		'question': question
	}
	
	return render(
		request=request,
		template_name="polls/detail.html",
		context=context
	)


def result(request, question_id):
	return HttpResponse(f'Estas viendo los resultados de la pregunta numero {question_id}')


def vote(request, question_id):
	return HttpResponse(f'Estas votando a la pregunta numero {question_id}')
