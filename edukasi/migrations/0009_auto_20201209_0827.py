# Generated by Django 3.1.2 on 2020-12-09 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edukasi', '0008_komplit_soal_tagsoal_ujian'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='tugas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='edukasi.ujian'),
        ),
        migrations.AlterField(
            model_name='soal',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='edukasi.TagSoal'),
        ),
    ]
