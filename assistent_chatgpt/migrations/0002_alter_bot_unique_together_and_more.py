# Generated by Django 4.2.7 on 2024-01-24 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistent_chatgpt', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bot',
            unique_together={('business', 'origin')},
        ),
        migrations.AlterUniqueTogether(
            name='instruction',
            unique_together={('business', 'index')},
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('business', 'key', 'origin')},
        ),
    ]