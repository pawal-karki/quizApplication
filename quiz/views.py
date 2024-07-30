from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from .serializers import QuestionSerializer
from rest_framework.status import HTTP_201_CREATED , HTTP_400_BAD_REQUEST , HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Question
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
    level = request.query_params.get('level')
    
    if level:
        if level not in ['easy', 'medium', 'hard']:
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

