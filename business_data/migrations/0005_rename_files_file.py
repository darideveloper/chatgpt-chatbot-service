# Generated by Django 4.2.7 on 2024-01-26 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistent_chatgpt', '0003_alter_business_options'),
        ('business_data', '0004_files'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Files',
            new_name='File',
        ),
    ]