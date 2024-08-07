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

class AnswerSerializer(serializers.Serializer): # Serializer is used because we are not saving the data in database
    question_attempt_id = serializers.IntegerField() #
    selected_option_id = serializers.IntegerField()

class QuizSubmissionSerializers(serializers.Serializer):
    quiz_attempt_id = serializers.IntegerField()
    answers = AnswerSerializer(many=True)


    def update(self, instance, validated_data):
        """
        Update the instance of Quiz Attempt.
        """
        answers = validated_data.get('answers')
        total_score = 0
        for answer in answers:
            question_attempt_id = answer.get('question_attempt_id')
            selected_option_id = answer.get('selected_option_id')

            try:
                question_attempt = QuestionAttemptDetails.objects.get(id=question_attempt_id, quiz_attempt=instance)
            except QuestionAttemptDetails.DoesNotExist:
                continue # if question_attempt_id is not found then continue will skip the current iteration and move to next iteration
            selected_option = Options.objects.get(id=selected_option_id)

            #update the selected option to question attempt
            question_attempt.selected_option = selected_option

            #update the isCorrect option of question attempt model
            question_attempt.is_correct = selected_option.isCorrect
            #save changes to the database
            question_attempt.save()

            #check if userSelected correct option
            if selected_option.isCorrect:
                total_score += 1
        
        #update total_score in quiz attempt 

        instance.total_score = total_score
        instance.save()
        return {'score' : total_score}

class UserLeaderboardSerializer(serializers.Serializer):
    username = serializers.CharField(source='user_name')
    total_score = serializers.IntegerField()
            

    





    

