# Generated by Django 4.2.5 on 2023-10-12 02:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0031_alter_producto_codigo_barras_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='codigo_barras',
            field=models.CharField(default='56735d1d74e6466bbb1335851477e135', max_length=50),
        ),
    ]
