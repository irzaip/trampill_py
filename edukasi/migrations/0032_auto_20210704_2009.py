# Generated by Django 3.1.2 on 2021-07-04 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0031_auto_20210704_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pengajar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=200)),
                ('lokasi', models.CharField(max_length=200, null=True)),
                ('deskripsi', models.TextField()),
                ('bank', models.CharField(max_length=200)),
                ('no_akun', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='kegiatan',
            name='url_donasi',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
