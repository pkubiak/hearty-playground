# Generated by Django 3.0 on 2020-02-07 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help_app', '0001_squashed_0008_auto_20200122_2348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='article',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]