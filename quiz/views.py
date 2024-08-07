from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from .serializers import QuestionSerializer , QuestionAttemptDetails , QuizAttemptSerializer , QuizSubmissionSerializers
from rest_framework.status import HTTP_201_CREATED , HTTP_400_BAD_REQUEST , HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question , QuizAttempt
from django.db.models import Sum

# from django.shortcuts import get_object_or_404
#decorators are the function that takes another function and extends the behavior of the latter function without explicitly modifying it.


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_questions(request):
    serializer = QuestionSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({**serializer.data,'message':'Question created successfully','status':HTTP_201_CREATED})
    return JsonResponse(serializer.errors, status = HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_questions(request):
    level = request.query_params.get('level') #get the level from the query parameter based on level i.e. the url will be /api/quiz/questions/get-questions/?level=hard
    valid_levels = ['easy', 'medium', 'hard']
    if level:
        if level not in valid_levels:
            return JsonResponse({'error': 'Invalid level specified'}, status=HTTP_400_BAD_REQUEST)
        questions = Question.objects.filter(level=level)[:20]
    else:
        questions = Question.objects.all()[:20]
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=HTTP_200_OK)
        
    
@api_view(['GET'])
def get_question_by_id(request, id):
    question = Question.objects.filter(pk=id)
    serializer = QuestionSerializer(instance=question , many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
def get_questions_by_category(request):
    category = request.query_params.get('category') #get the level from the query parameter based on level i.e. the url will be /api/quiz/questions/get-questions/?level=hard
    valid_categories = ['Computer Science', 'Science', 'Literature']
    if category:
        if category not in valid_categories:
            return JsonResponse({'error': 'Invalid category specified'}, status=HTTP_400_BAD_REQUEST)
        questions = Question.objects.filter(category=category)[:20]
    else:
        questions = Question.objects.all()[:20]
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quiz_attempt(request):
    serializers = QuizAttemptSerializer(data = request.data, context={'request':request})
    if serializers.is_valid():
        serializers.save()
        return JsonResponse({**serializers.data,'message':'Quiz Attempt created successfully','status':HTTP_201_CREATED})
    
    return JsonResponse(serializers.errors, status = HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request):
    serializers = QuizSubmissionSerializers(data = request.data)
    if serializers.is_valid():
        quiz_attempt_id = serializers.validated_data.get('quiz_attempt_id')
        try:
            quiz_attempt = QuizAttempt.objects.get(id=quiz_attempt_id, user = request.user)
            score = serializers.update(quiz_attempt, serializers.validated_data)
            return Response(score, status = HTTP_201_CREATED)
    

        except QuizAttempt.DoesNotExist:
            return JsonResponse({'error': 'attempt does not exist'}, status=HTTP_400_BAD_REQUEST)
        
    return JsonResponse(serializers.errors , status = HTTP_400_BAD_REQUEST)

# get attempt by user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attempt_by_user(request):
    try:
        quiz_attempt = QuizAttempt.objects.filter(user = request.user)
        serializer = QuizAttemptSerializer(quiz_attempt, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    except QuizAttempt.DoesNotExist:
        return JsonResponse({'error': 'attempt does not exist'}, status=HTTP_400_BAD_REQUEST)

# get attempt by id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attempt_by_id(request, id):
    try:
        quiz_attempt = QuizAttempt.objects.filter(id=id, user = request.user)
        serializer = QuizAttemptSerializer(quiz_attempt)
        return Response(serializer.data, status=HTTP_200_OK)
    
    except QuizAttempt.DoesNotExist:
        return JsonResponse({'error': 'attempt does not exist'}, status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])

def get_leaderboard(request):
    try:
        leaderboard = QuizAttempt.objects.values('user').annotate(total_score=Sum('total_score')).order_by('-total_score')[:10]
        serializer = QuizAttemptSerializer(leaderboard, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
    