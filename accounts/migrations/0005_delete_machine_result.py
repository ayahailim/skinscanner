# Generated by Django 4.2.1 on 2023-05-18 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_machine_result_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='machine_result',
        ),
    ]
