# Generated by Django 4.2.7 on 2024-02-07 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socials_chatbots', '0004_welcomemessage_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='welcomemessage',
            name='message',
            field=models.TextField(),
        ),
    ]