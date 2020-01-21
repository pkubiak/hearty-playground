# Generated by Django 3.0 on 2020-01-21 05:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('activity_quiz', '0004_auto_20200121_0442'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activity_quiz.Question')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('activity_quiz.question',),
        ),
        migrations.CreateModel(
            name='MultipleChoiceAnswer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('score', models.IntegerField(default=0)),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_set', to='activity_quiz.MultipleChoiceQuestion')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]