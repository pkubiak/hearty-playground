# Generated by Django 3.0 on 2020-01-23 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0018_auto_20200123_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='score',
            field=models.FloatField(null=True),
        ),
    ]
