from django.urls import path
from .views import create_question , get_questions

urlpatterns = [
    path('question/create/',create_question , name='create-question'),
    path('question/get-questions/', get_questions , name='get-questions')
]