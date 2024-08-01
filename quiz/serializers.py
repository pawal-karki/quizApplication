from .models import Options , Question , QuestionAttemptDetails , QuizAttempt
from rest_framework import serializers

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields =['id', 'option', 'isCorrect']
        required = ['option', 'isCorrect'] # all fields are required otherwise error will be thrown

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True) # 
    class Meta:
        model = Question
        fields = ['id', 'question', 'category', 'level', 'options']
        required = ['question', 'category', 'level', 'options']

    def create(self,validated_data):
        options = validated_data.pop('options')
        question = Question.objects.create(**validated_data)

        for option in options:
            Options.objects.create(questionId=question, **option)
        return question
    
class QuestionAttemptDetailsSerializer(serializers.ModelSerializer):
    question = QuestionSerializer() # one to one relationship
    class Meta:
        model = QuestionAttemptDetails
        fields = ['id','question','is_correct', ]

class QuizAttemptSerializer(serializers.ModelSerializer):
    questions_attempt = QuestionAttemptDetailsSerializer(many=True , read_only = True) # many = True because it has one to many relationship
    class Meta:
        model = QuizAttempt
        fields = ['id', 'attempted_date_time','questions_attempt' ,'total_score'  ]
    
    def create(self , validated_data ):
        user = self.context['request'].user
        quiz_attempt = QuizAttempt.objects.create(user=user)

        questions = Question.objects.all().order_by('?')[:15]
        for question in questions:
            QuestionAttemptDetails.objects.create(question=question, quiz_attempt=quiz_attempt)
        return quiz_attempt



