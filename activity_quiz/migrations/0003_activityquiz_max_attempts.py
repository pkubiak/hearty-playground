# Generated by Django 3.0 on 2020-01-21 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_quiz', '0002_auto_20200121_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityquiz',
            name='max_attempts',
            field=models.PositiveIntegerField(default=1),
        ),
    ]