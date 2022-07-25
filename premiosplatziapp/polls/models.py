""" polls models """
from django.db import models

# Create your models here.
class Question(models.Model):
	# Usamos CharField para decir que un question text sera equivalente
	# a un varchar en la base de datos
	question_text = models.CharField(max_length=200)
	pub_data = models.DateTimeField("date published")


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
