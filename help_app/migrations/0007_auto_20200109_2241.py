# Generated by Django 3.0 on 2020-01-09 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help_app', '0006_remove_article_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]