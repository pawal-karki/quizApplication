from django.urls import path
from .views import create_questions , get_questions , get_question_by_id , get_questions_by_category

urlpatterns = [
    path('questions/create/',create_questions , name='create-question'),
    path('questions/get-questions/', get_questions , name='get-questions'),
    path('questions/get-question-by-id/<int:id>', get_question_by_id , name='get-question-by-id'),
    path('questions/get-question-by-category/<str:category>', get_questions_by_category , name='get-questions-by-category')
]