# Generated by Django 3.0 on 2020-01-14 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_note', '0009_auto_20200114_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitynote',
            name='completable',
            field=models.BooleanField(choices=[(True, 'YES'), (False, 'NO')], default=False),
        ),
    ]
