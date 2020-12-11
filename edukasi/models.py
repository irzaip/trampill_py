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
    gambar = models.ImageField(null=True, blank=True)
    kategori = models.CharField(max_length=100, choices=KATEGORI)
    tags = models.ManyToManyField(Tag)
    summary = models.TextField()
    harga = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    pengajar = models.CharField(max_length=40, null=True)
    tentang_pengajar = models.TextField(null=True)

    def __str__(self):
        return self.judul

class Ujian(models.Model):
    judul = models.CharField(max_length=25)
    kode = models.CharField(max_length=10, null=True, blank=True)
    deskripsi = models.TextField()
    nilai_max = models.IntegerField(default=100)

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
    tugas = models.ForeignKey(Ujian, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + str("-") + str(self.materi) + str("-") + str(self.no_urut) + str("-") + str(self.judul)

    
class Pengumuman(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    judul = models.CharField(max_length=100,null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    isi = models.TextField()
    display = models.BooleanField(default=False)
    frontpage = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)

class Message(models.Model):
     sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
     reciever = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
     msg_content = models.TextField()
     readed = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True, null=True)



class TagSoal(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Soal(models.Model):
    TIPE = (
        ('Pilihan Ganda', 'Pilihan Ganda'),
        ('Betul / Salah', 'Betul / Salah'),
        ('Mencocokkan', 'Mencocokkan'),
        ('Jawab singkat', 'Jawab singkat'),
        ('Numerik', 'Numerik'),
        ('Essay', 'Essay'),
        ('Kumpul URL', 'Kumpul URL'),
        ('Lain-lain', 'Lain-lain'),
    )
    ujian = models.ForeignKey(Ujian, on_delete=models.CASCADE )
    no_urut = models.IntegerField()
    tipe = models.CharField(max_length=20, choices=TIPE)
    judul = models.CharField(max_length=25)
    pertanyaan = models.TextField()
    penjelasan = models.TextField()
    benarsalah = models.BooleanField(null=True, blank=True)
    multianswer = models.BooleanField(null=True, blank=True, default=False)
    tags = models.ManyToManyField(TagSoal)
    jawaban_url = models.CharField(max_length=100, null=True)
    jawaban_essay = models.TextField(null=True)
    jawaban_a = models.TextField(max_length=30, null=True, blank=True)
    jawaban_b = models.TextField(max_length=30, null=True, blank=True)
    jawaban_c = models.TextField(max_length=30, null=True, blank=True)
    jawaban_d = models.TextField(max_length=30, null=True, blank=True)
    jawaban_e = models.TextField(max_length=30, null=True, blank=True)
    jawaban_f = models.TextField(max_length=30, null=True, blank=True)
    jawaban_g = models.TextField(max_length=30, null=True, blank=True)
    jawaban_h = models.TextField(max_length=30, null=True, blank=True)
    jawaban_1 = models.TextField(max_length=30, null=True, blank=True)
    jawaban_2 = models.TextField(max_length=30, null=True, blank=True)
    jawaban_3 = models.TextField(max_length=30, null=True, blank=True)
    jawaban_4 = models.TextField(max_length=30, null=True, blank=True)
    jawaban_5 = models.TextField(max_length=30, null=True, blank=True)
    jawaban_6 = models.TextField(max_length=30, null=True, blank=True)
    jawaban_7 = models.TextField(max_length=30, null=True, blank=True)
    jawaban_8 = models.TextField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.judul

class Komplit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + "-" + self.topic.judul

class Diskusi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    pesan = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username + "-" + self.topic.judul

class Pembayaran(models.Model):
    STATUS = (
        ('posted', 'posted'),
        ('blm diperiksa', 'blm diperiksa'),
        ('disetujui', 'disetujui'),
        ('ditolak', 'ditolak'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE)
    harga = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    no_order = models.CharField(max_length=10)    
    status = models.CharField(max_length=20, default='posted')


class Pendaftaran(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE)


class Favorit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE)

