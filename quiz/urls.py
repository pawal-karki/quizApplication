from django.urls import path
from .views import create_questions , get_questions , get_question_by_id , get_questions_by_category, create_quiz_attempt , submit_quiz ,get_attempt_by_user,get_attempt_by_id, get_leaderboard
urlpatterns = [
    path('questions/create/',create_questions , name='create-question'),
    path('questions/get-questions/', get_questions , name='get-questions'),
    path('questions/get-question-by-id/<int:id>', get_question_by_id , name='get-question-by-id'),
    path('questions/get-question-by-category/<str:category>', get_questions_by_category , name='get-questions-by-category'),
    path('attempt/create/',create_quiz_attempt , name='create-quiz-attempt'),
    path('submit/quiz/',submit_quiz, name='submit-quiz'),
    path('attempt/get-attempt-by-user/',get_attempt_by_user, name='get-attempt-by-user'),
    path('attempt/get-attempt-by-id/<int:id>',get_attempt_by_id, name='get-attempt-by-id'),
    path('leaderboard/', get_leaderboard, name='leaderboard')

]