# Generated by Django 5.0.7 on 2024-11-08 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0005_alter_participant_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='nickname',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]