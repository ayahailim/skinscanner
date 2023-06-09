# Generated by Django 4.2.1 on 2023-05-18 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='classifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='image/classifier/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('prediction', models.CharField(max_length=50)),
            ],
        ),
    ]
