# Generated by Django 3.0 on 2020-01-11 03:34

import course_app.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='banner',
            field=models.ImageField(null=True, upload_to=course_app.models.course_directory_path),
        ),
        migrations.AlterField(
            model_name='course',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), blank=True, null=True, size=None),
        ),
    ]
