# Generated by Django 3.0 on 2019-12-15 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('help_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='order',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='article',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='help_app.Article'),
        ),
    ]
