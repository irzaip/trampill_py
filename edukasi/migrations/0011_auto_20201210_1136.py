# Generated by Django 3.1.2 on 2020-12-10 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('edukasi', '0010_diskusi'),
    ]

    operations = [
        migrations.AddField(
            model_name='materi',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='materi',
            name='harga',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='materi',
            name='pengajar',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='materi',
            name='tentang_pengajar',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_1',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_2',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_3',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_4',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_5',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_6',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_7',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_8',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_a',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_b',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_c',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_d',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_e',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_f',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_g',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='soal',
            name='jawaban_h',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.CreateModel(
            name='Pendaftaran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edukasi.materi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pembayaran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harga', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('no_order', models.CharField(max_length=10)),
                ('status', models.CharField(default='posted', max_length=20)),
                ('materi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edukasi.materi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favorit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edukasi.materi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
