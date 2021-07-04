# Generated by Django 3.1.2 on 2021-07-04 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0030_kegiatan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Penyelenggara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_penyelenggara', models.CharField(max_length=200, null=True)),
                ('alamat_penyelenggara', models.TextField()),
                ('status', models.CharField(choices=[('belum terverifikasi', 'belum terverifikasi'), ('terverifikasi', 'terverifikasi'), ('pending', 'pending')], max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='kegiatan',
            name='jadwal',
        ),
        migrations.AddField(
            model_name='kegiatan',
            name='judul_acara',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='kegiatan',
            name='status_acara',
            field=models.CharField(choices=[('belum terverifikasi', 'belum terverifikasi'), ('terverifikasi', 'terverifikasi'), ('pending', 'pending')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='kegiatan',
            name='url_donasi',
            field=models.CharField(max_length=300),
        ),
        migrations.AddField(
            model_name='kegiatan',
            name='penyelenggara',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='edukasi.penyelenggara'),
        ),
    ]
