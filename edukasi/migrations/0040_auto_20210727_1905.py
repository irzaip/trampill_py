# Generated by Django 3.1.2 on 2021-07-27 12:05

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0039_auto_20210718_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ring_getter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ring_name', models.CharField(blank=True, max_length=200, null=True)),
                ('ring_ref', models.CharField(blank=True, max_length=200, null=True)),
                ('ring_url', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='pengajar',
            name='ewallet',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='kegiatan',
            name='deskripsi',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='ulasan',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.CreateModel(
            name='RingKegiatan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ring_ref', models.CharField(blank=True, max_length=200, null=True)),
                ('judul_acara', models.CharField(max_length=200, null=True)),
                ('status_acara', models.CharField(choices=[('belum terverifikasi', 'belum terverifikasi'), ('terverifikasi', 'terverifikasi'), ('pending', 'pending')], max_length=100, null=True)),
                ('lokasi', models.CharField(blank=True, max_length=200, null=True)),
                ('deskripsi', ckeditor.fields.RichTextField()),
                ('rating', models.IntegerField(choices=[(1, '*'), (2, '**'), (3, '***'), (4, '****'), (5, '*****')], default='5')),
                ('tanggal_mulai', models.DateTimeField(null=True)),
                ('tanggal_selesai', models.DateTimeField(null=True)),
                ('url_donasi', models.CharField(max_length=300, null=True)),
                ('materi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='edukasi.materi')),
                ('penyelenggara', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='edukasi.penyelenggara')),
            ],
        ),
    ]
