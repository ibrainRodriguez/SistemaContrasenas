# Generated by Django 3.2.4 on 2021-06-20 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0005_alter_usuarios_contra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='contra',
            field=models.CharField(max_length=200),
        ),
    ]
