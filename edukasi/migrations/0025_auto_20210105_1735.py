# Generated by Django 3.1.2 on 2021-01-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0024_auto_20210104_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materi',
            name='tags',
            field=models.ManyToManyField(blank=True, to='edukasi.Tag'),
        ),
    ]