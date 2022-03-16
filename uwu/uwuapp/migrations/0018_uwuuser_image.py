# Generated by Django 3.2.12 on 2022-03-16 07:58

from django.db import migrations, models
import uwu.uwuapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('uwuapp', '0017_manga_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='uwuuser',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to=uwu.uwuapp.models.upload_to, verbose_name='Image'),
        ),
    ]
