# Generated by Django 3.0 on 2020-01-21 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_quiz', '0006_openanswer_openquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='openquestion',
            name='placeholder',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
