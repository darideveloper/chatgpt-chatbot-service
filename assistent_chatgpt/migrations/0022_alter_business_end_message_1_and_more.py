# Generated by Django 4.2.7 on 2024-03-20 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistent_chatgpt', '0021_alter_user_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='end_message_1',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='end_message_2',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]