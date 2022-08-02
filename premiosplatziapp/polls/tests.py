""" polls tests """
# Python
import datetime

# Django
from django.test import TestCase
from django.utils import timezone

# Models
from .models import Question

# Create your tests here.
# podemos testar modelos y vistas y mas
class QuestionModelTests(TestCase):
	""" Bateria de tests """
	def test_was_publish_recently_with_future_questionos(self):
		""" was_published_recently returns false for questions whose pub_date is in the future """
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(question_text="¿Quien es el mejor curse director de platzi?", pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_publish_recently_with_past_questionos(self):
		""" was_published_recently returns false for questions whose pub_date is in the past """
		time = timezone.now() + datetime.timedelta(days=-30)
		past_question = Question(question_text="¿Pregunta del pasado?", pub_date=time)
		self.assertIs(past_question.was_published_recently(), False)

	def test_was_publish_recently_with_present_questionos(self):
		""" was_published_recently returns true for questions whose pub_date is today """
		time = timezone.now()
		past_question = Question(question_text="¿Pregunta hoy?", pub_date=time)
		self.assertIs(past_question.was_published_recently(), True)
