""" polls admin """
# Django
from django.contrib import admin

# Models
from .models import Question, Choice

class ChoiceInline(admin.StackedInline):
	"""
	Clase para conbinar la creación de un modelo con otro
	"""
	model = Choice
	extra = 3


class QuestionAdmin(admin.ModelAdmin):
	""" 
	clase que nos sirve para personalizar como se ve el modelo en la pagina de admin
	"""
	# Cambiamos el orden de los campos
	fields = ["pub_date", "question_text"]
	inlines = [ChoiceInline]
	list_display = ("question_text", "pub_date", "was_published_recently")
	list_filter = ["pub_date"]
	search_fields = ["question_text"]


# Register your models here.
admin.site.register(Question, QuestionAdmin)
