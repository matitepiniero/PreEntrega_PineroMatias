# Generated by Django 4.2.5 on 2023-10-09 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0026_alter_producto_codigo_barras'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile_picture',
            new_name='avatar',
        ),
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default_avatar.png', null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='codigo_barras',
            field=models.CharField(default='8dc44367bdc24c219df9b8f92650df9e', max_length=50),
        ),
    ]
