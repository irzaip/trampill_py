# Generated by Django 3.1.2 on 2020-12-05 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0006_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materi',
            name='gambar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.DeleteModel(
            name='Notifikasi',
        ),
    ]
