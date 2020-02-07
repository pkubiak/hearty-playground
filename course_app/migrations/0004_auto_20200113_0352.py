# Generated by Django 3.0 on 2020-01-13 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0003_auto_20200113_0324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]
