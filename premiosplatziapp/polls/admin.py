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


# Register your models here.
admin.site.register(Question, QuestionAdmin)
