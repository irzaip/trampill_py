# Generated by Django 3.1.2 on 2021-09-07 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0041_materi_ytb_playlist_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
