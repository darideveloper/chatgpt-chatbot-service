# Generated by Django 4.2.7 on 2024-02-08 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_data', '0012_rename_compoatibility_refaccionariagonzales_compatibility'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refaccionariagonzales',
            old_name='descripcion',
            new_name='description',
        ),
    ]