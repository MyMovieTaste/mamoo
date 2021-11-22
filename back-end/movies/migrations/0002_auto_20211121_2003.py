# Generated by Django 3.2.9 on 2021-11-21 20:03

from django.db import migrations, models
import django.db.models.deletion


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
            model_name='movie',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.year'),
        ),
    ]