# Generated by Django 3.1.2 on 2020-11-28 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('edukasi', '0002_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='materi',
            name='gambar',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='materi',
            name='deskripsi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='isi_tambahan',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='link',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='no_urut',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Notifikasi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isi', models.TextField(null=True)),
                ('read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
