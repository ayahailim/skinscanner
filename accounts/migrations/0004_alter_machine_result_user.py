# Generated by Django 4.2.1 on 2023-05-14 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_machine_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine_result',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userresult', to=settings.AUTH_USER_MODEL),
        ),
    ]
