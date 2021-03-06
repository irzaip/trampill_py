# Generated by Django 3.1.2 on 2021-07-04 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0029_auto_20210114_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kegiatan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deskripsi', models.TextField()),
                ('rating', models.IntegerField(choices=[(1, '*'), (2, '**'), (3, '***'), (4, '****'), (5, '*****')], default='5')),
                ('tanggal_mulai', models.DateTimeField(auto_now_add=True, null=True)),
                ('tanggal_selesai', models.DateTimeField(auto_now_add=True, null=True)),
                ('jadwal', models.TextField()),
                ('url_donasi', models.TextField()),
                ('materi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='edukasi.materi')),
            ],
        ),
    ]
