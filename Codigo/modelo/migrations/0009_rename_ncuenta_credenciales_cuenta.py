# Generated by Django 3.2.4 on 2021-06-21 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0008_credenciales'),
    ]

    operations = [
        migrations.RenameField(
            model_name='credenciales',
            old_name='ncuenta',
            new_name='cuenta',
        ),
    ]
