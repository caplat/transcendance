# Generated by Django 5.0.7 on 2024-11-08 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='date',
        ),
    ]