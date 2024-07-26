from django.db import models

# Create your models here. for database table creation
class Question(models.Model):
    question = models.TextField()
    category = models.TextField()
    level = models.TextField()

class Options(models.Model):
    option = models.TextField()
    isCorrect = models.BooleanField()
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='options')





