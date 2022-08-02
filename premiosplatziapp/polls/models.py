""" polls models """
# Python
import datetime

# Django
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	# Usamos CharField para decir que un question text sera equivalente
	# a un varchar en la base de datos
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField("date published")

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		""" Returns true if the pub_date isn't 24 hours pass yet """
		return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text
