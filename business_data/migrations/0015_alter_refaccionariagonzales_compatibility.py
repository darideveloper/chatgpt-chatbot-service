# Generated by Django 4.2.7 on 2024-02-08 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_data', '0014_remove_refaccionariagonzales_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refaccionariagonzales',
            name='compatibility',
            field=models.TextField(),
        ),
    ]
