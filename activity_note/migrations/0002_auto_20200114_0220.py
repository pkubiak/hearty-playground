# Generated by Django 3.0 on 2020-01-14 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_note', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NoteContent',
            new_name='ActivityNote',
        ),
    ]