from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import QuestionSerializer
from rest_framework.status import HTTP_201_CREATED , HTTP_400_BAD_REQUEST



# Create your views here.
@api_view(['POST'])
def create_question(request):
    serializer = QuestionSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({**serializer.data,'message':'Question created successfully','status':HTTP_201_CREATED})
    return JsonResponse(serializer.errors, status = HTTP_400_BAD_REQUEST)
    
    

