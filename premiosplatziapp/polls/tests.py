""" polls tests """
# Python
import datetime

# Django
from django.test import TestCase
from django.utils import timezone
from django.shortcuts import reverse

# Models
from .models import Question

# Functions
def create_question(question_text, days):
	"""
	Create a question with the given "question_text", adn published the given
	number of days offset to now.
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

# Create your tests here.
# podemos testar modelos y vistas y mas
class QuestionModelTests(TestCase):
	""" Bateria de tests para modelos """
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


class QuestionIndexViewTests(TestCase):
	""" Bateria de tests para la vista index """
	def test_no_questions(self):
		""" If no question exist, an appropiete message is displayed """
		response = self.client.get(reverse("polls:index"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are availabe.")
		self.assertQuerysetEqual(response.context["latest_question_list"], [])

	def test_future_questions(self):
		"""
		Questions with a pub_date in the future aren't published in the index
		"""
		create_question("Future question", days=30)
		response = self.client.get(reverse("polls:index"))
		self.assertContains(response, "No polls are availabe.")
		self.assertQuerysetEqual(response.context["latest_question_list"], [])

	def test_past_question(self):
		"""
		Questions with a pub_date in the past should be published in the index
		"""
		question = create_question("past question", days=-10)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerysetEqual(response.context["latest_question_list"], [question])

	def test_future_question_and_past_question(self):
		"""
		Even if both past and future question exist, only past questions are displayed.
		"""
		past_question = create_question(question_text="Past question", days=-30)
		future_question = create_question(question_text="future question", days=30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerysetEqual(
			response.context["latest_question_list"],
			[past_question]
		)

	def test_two_past_questions(self):
		"""
		The questions index page may display multiple questions.
		"""
		past_question1 = create_question(question_text="Past1 question", days=-30)
		past_question2 = create_question(question_text="Past2 question", days=-40)
		response = self.client.get(reverse("polls:index"))

		self.assertQuerysetEqual(
			response.context["latest_question_list"],
			[past_question1, past_question2]
		)

	def test_two_future_questions(self):
		"""
		if two future question was created, the response context must be empty
		"""
		_ = create_question(question_text="future1 question", days=30)
		_ = create_question(question_text="future2 question", days=30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerysetEqual(
			response.context["latest_question_list"],
			[]
		)


class QuestionMyDetailViewTests(TestCase):
	""" Bateria de tests para MydetailView"""
	def test_future_questions(self):
		"""
		The detail view of a question with a pub_date in the future
		returs a 404 error not found
		"""
		future_question = create_question(question_text="future question", days=30)
		url = reverse("polls:detail", args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		"""
		The detail view of a question with a pub_date in the past
		Displays the question's text
		"""
		past_question = create_question(question_text="past question", days=-30)
		url = reverse("polls:detail", args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)
