# Generated by Django 4.2.7 on 2024-02-19 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistent_chatgpt', '0009_rename_datafiles_datafile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DataFile',
        ),
    ]
