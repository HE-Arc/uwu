# Generated by Django 3.2.12 on 2022-03-01 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('is_finished', models.BooleanField()),
            ],
        ),
    ]
