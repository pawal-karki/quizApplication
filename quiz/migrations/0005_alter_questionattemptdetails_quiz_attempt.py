# Generated by Django 5.0.7 on 2024-08-01 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quizattempt_questionattemptdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionattemptdetails',
            name='quiz_attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_attempt', to='quiz.quizattempt'),
        ),
    ]
