# Generated by Django 3.1.2 on 2021-01-14 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0028_auto_20210114_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='review',
            new_name='rating',
        ),
    ]
