# Generated by Django 3.0 on 2020-01-14 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_note', '0006_auto_20200114_0527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noteactivity',
            name='completable',
        ),
    ]
