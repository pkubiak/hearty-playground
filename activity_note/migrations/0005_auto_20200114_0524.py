# Generated by Django 3.0 on 2020-01-14 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0011_auto_20200114_0524'),
        ('activity_note', '0004_auto_20200114_0426'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteActivity',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='course_app.Activity')),
                ('text', models.TextField()),
                ('completable', models.BooleanField(choices=[(True, 'YES'), (False, 'NO')], default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('course_app.activity',),
        ),
        migrations.DeleteModel(
            name='ActivityNote',
        ),
    ]