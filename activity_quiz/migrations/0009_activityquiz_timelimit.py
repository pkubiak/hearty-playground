# Generated by Django 3.0 on 2020-01-21 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_quiz', '0008_solutionquiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityquiz',
            name='timelimit',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
