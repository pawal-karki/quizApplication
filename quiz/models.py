from django.db import models
from django.contrib.auth.models import User
# Create your models here. for database table creation
class Question(models.Model):
    question = models.TextField()
    category = models.TextField()
    level = models.TextField()

class Options(models.Model):
    option = models.TextField()
    isCorrect = models.BooleanField()
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='options')

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempted_date_time = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField(default = 0) 

class QuestionAttemptDetails(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE , related_name='questions_attempt')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Options,blank=True,null=True,on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

