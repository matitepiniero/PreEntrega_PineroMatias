# Generated by Django 4.2.5 on 2023-10-06 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0008_alter_deposito_id_alter_producto_codigo_barras'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo_barras',
            field=models.CharField(default='464dfe0da1764690a53f069d7356cc30', max_length=50),
        ),
    ]
