from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from .serializers import QuestionSerializer
from rest_framework.status import HTTP_201_CREATED , HTTP_400_BAD_REQUEST , HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from .models import Question
#decorators are the function that takes another function and extends the behavior of the latter function without explicitly modifying it.


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    serializer = QuestionSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({**serializer.data,'message':'Question created successfully','status':HTTP_201_CREATED})
    return JsonResponse(serializer.errors, status = HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_questions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(data=questions)
    return JsonResponse(serializer.data, status=HTTP_200_OK)

    

