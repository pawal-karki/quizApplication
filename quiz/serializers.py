from .models import Options , Question
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