from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Create your models here.
class UserExt(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    kota = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
 
    def __str__(self):
      return self.user.first_name + "(" + str(self.user.email) + ")"

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Materi(models.Model):
    KATEGORI = (
        ('Teknologi', 'Teknologi'),
        ('Bisnis', 'Bisnis'),
        ('Pengembangan Diri', 'Pengembangan Diri'),
        ('Batch Khusus', 'Batch Khusus'),
        ('Koding Playlist', 'Koding Playlist'),
        ('Projects', 'Projects'),
    )

    judul = models.CharField(max_length=200)
    kode = models.CharField(max_length=20, null=True)
    deskripsi = models.TextField(null=True, blank=True)
    gambar = models.ImageField()
    kategori = models.CharField(max_length=100, choices=KATEGORI)
    tags = models.ManyToManyField(Tag)
    summary = models.TextField()

    def __str__(self):
        return self.judul

class Topic(models.Model):
    JENIS = (
        ('Label', 'Label'),
        ('Link Video', 'Link Video'),
        ('Konten Umum', 'Konten Umum'),
        ('Tugas', 'Tugas'),
        ('Quiz', 'Quiz'),
        ('Feedback', 'Feedback'),
        ('Url luar', 'Url luar'),
        ('File', 'File'),
    )

    materi = models.ForeignKey(Materi, null=True, on_delete=models.CASCADE)
    no_urut = models.IntegerField()
    judul = models.CharField(max_length = 50)
    jenis = models.CharField(max_length=20, choices=JENIS)
    link = models.CharField(max_length=250, null=True, blank=True)
    isi_tambahan = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + str("-") + str(self.materi) + str("-") + str(self.no_urut) + str("-") + str(self.judul)

class Notifikasi(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    isi = models.TextField(null=True,)
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " - "  + str(self.isi)
    
class Pengumuman(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    judul = models.CharField(max_length=100,null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    isi = models.TextField()
    display = models.BooleanField(default=False)
    frontpage = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)