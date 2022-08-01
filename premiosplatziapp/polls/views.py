""" Polls views """
# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.views.generic import ListView, DetailView

# Models
from .models import Question, Choice

# Create your views here.

class IndexView(ListView):
	template_name = "polls/index.html"
	context_object_name = "latest_question_list"

	def get_queryset(self):
		""" Return The last five published questions """
		return Question.objects.order_by("-pub_date")[:5]


class MyDetailView(DetailView):
	template_name = "polls/detail.html"
	model = Question


class ResultView(DetailView):
	template_name = "polls/results.html"
	model = Question

# def index(request):
# 	latest_question_list = Question.objects.all()
# 	context = {
# 		'latest_question_list': latest_question_list
# 	}
# 	return render(
# 		request=request,
# 		template_name="polls/index.html",
# 		context=context
# 	)


# def detail(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	context = {
# 		'question': question
# 	}
	
# 	return render(
# 		request=request,
# 		template_name="polls/detail.html",
# 		context=context
# 	)


# def result(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	context = {
# 		"question": question
# 	}
# 	return render(
# 		request=request,
# 		template_name="polls/results.html",
# 		context=context
# 	)


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	try:
		selected_choice = question.choice_set.get(pk=request.POST["choice"])
	except (KeyError, Choice.DoesNotExist):
		context = {
			"question": question,
			"error_message": "No elegiste una respuesta"
		}
		return render(
			request=request, 
			template_name="polls/detail.html",
			context=context
		)
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

	return HttpResponse(f'Estas votando a la pregunta numero {question_id}')
