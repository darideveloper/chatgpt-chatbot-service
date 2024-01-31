# Generated by Django 4.2.7 on 2024-01-31 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_data', '0009_remove_refaccionariax_bussiness'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefaccionariaY',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fabricante', models.CharField(max_length=100)),
                ('numero_de_pieza', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=100)),
                ('precio', models.FloatField()),
                ('cantidad_en_stock', models.IntegerField()),
                ('ubicacion', models.CharField(max_length=100)),
                ('estante', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=100)),
                ('ano', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Refaccionaria Y Product',
                'verbose_name_plural': 'Refaccionaria Y Products',
            },
        ),
    ]
