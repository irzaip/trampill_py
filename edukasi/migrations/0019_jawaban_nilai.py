# Generated by Django 3.1.2 on 2020-12-17 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0018_jawaban'),
    ]

    operations = [
        migrations.AddField(
            model_name='jawaban',
            name='nilai',
            field=models.IntegerField(default=0),
        ),
    ]
