# Generated by Django 4.2.7 on 2024-01-31 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assistent_chatgpt', '0003_alter_business_options'),
        ('business_data', '0007_refaccionariax_bussiness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refaccionariax',
            name='bussiness',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistent_chatgpt.business'),
        ),
    ]