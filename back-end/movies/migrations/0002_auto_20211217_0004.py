# Generated by Django 3.2.9 on 2021-12-17 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='year',
            name='year',
        ),
        migrations.AddField(
            model_name='year',
            name='year_str',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
