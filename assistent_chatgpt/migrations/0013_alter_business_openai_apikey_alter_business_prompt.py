# Generated by Django 4.2.7 on 2024-03-15 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistent_chatgpt', '0012_business_prompt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='openai_apikey',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='business',
            name='prompt',
            field=models.TextField(default=''),
        ),
    ]
