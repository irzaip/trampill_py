# Generated by Django 3.1.2 on 2020-12-12 06:14

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0013_auto_20201211_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materi',
            name='deskripsi',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pembayaran',
            name='status',
            field=models.CharField(choices=[('posted', 'posted'), ('blm diperiksa', 'blm diperiksa'), ('disetujui', 'disetujui'), ('ditolak', 'ditolak')], default='posted', max_length=20),
        ),
    ]
