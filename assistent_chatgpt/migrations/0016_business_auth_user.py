# Generated by Django 4.2.7 on 2024-03-19 01:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assistent_chatgpt', '0015_alter_instruction_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='auth_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
