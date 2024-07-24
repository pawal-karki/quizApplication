from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.TextField()
    category = models.TextField()
    level = models.TextField()

class Options(models.Model):
    option = models.TextField()
    isCorrect = models.BooleanField()
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE)


