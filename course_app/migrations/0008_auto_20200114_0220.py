# Generated by Django 3.0 on 2020-01-14 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0007_auto_20200114_0110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['order'], 'verbose_name_plural': 'Activities'},
        ),
    ]
