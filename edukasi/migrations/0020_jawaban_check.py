# Generated by Django 3.1.2 on 2020-12-18 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0019_jawaban_nilai'),
    ]

    operations = [
        migrations.AddField(
            model_name='jawaban',
            name='check',
            field=models.BooleanField(default=False),
        ),
    ]
