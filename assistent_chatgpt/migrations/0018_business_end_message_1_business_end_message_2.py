# Generated by Django 4.2.7 on 2024-03-19 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistent_chatgpt', '0017_alter_business_auth_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='end_message_1',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='business',
            name='end_message_2',
            field=models.TextField(default=''),
        ),
    ]