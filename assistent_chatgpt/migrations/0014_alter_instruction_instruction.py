# Generated by Django 4.2.7 on 2024-03-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistent_chatgpt', '0013_alter_business_openai_apikey_alter_business_prompt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instruction',
            name='instruction',
            field=models.CharField(max_length=15000),
        ),
    ]
