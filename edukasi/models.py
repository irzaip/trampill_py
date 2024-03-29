from django.db import models
from django.contrib.auth.models import User
import string, random
from ckeditor.fields import RichTextField
from datetime import datetime

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))

class AkunBank(models.Model):
    nama_rekening = models.CharField(max_length=200, null=True, blank=True)
    nama_bank = models.CharField(max_length=200, null=True, blank=True)
    nama_cabang = models.CharField(max_length=200, null=True, blank=True)
    bank_code = models.CharField(max_length=200)


class Kategori(models.Model):
    nama_kategori = models.CharField(max_length=200, null=True, blank=True)
    
# Create your models here.
class Pengajar(models.Model):
    nama = models.CharField(max_length=200)
    lokasi = models.CharField(max_length=200, blank=True)
    tentang_pengajar = RichTextField(null=True, blank=True)
    bank = models.CharField(max_length=200, blank=True)
    no_akun = models.CharField(max_length=200, blank=True)
    ewallet = models.CharField(max_length=200, blank=True)

    @classmethod
    def create_pengajar(cls, nama, tentang_pengajar):
        pengajar = cls(nama=nama, tentang_pengajar=tentang_pengajar)
        return pengajar

    def __str__(self):
        return str(self.id)+"-"+self.nama

class UserExt(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    kota = models.CharField(max_length=200)
    kupon_account = models.CharField(max_length=200, default="")
    last_balance = models.DecimalField(max_digits=19, decimal_places=6, default=0)
    last_balance_created = models.DateTimeField(blank=True, default=datetime.now)
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
    RATING = (
        ('dasar','dasar'),
        ('menengah', 'menengah'),
        ('mahir','mahir'),
    )

    judul = models.CharField(max_length=200)
    kode = models.CharField(max_length=20, null=True)
    rating = models.CharField(max_length=20, default='dasar', choices=RATING)
    pendek = models.CharField(max_length=300,null=True)
    deskripsi = RichTextField(null=True, blank=True)
    gambar = models.ImageField(null=True, blank=True)
    kategori = models.CharField(max_length=100, default='Teknologi', choices=KATEGORI)
    tags = models.ManyToManyField(Tag, blank=True)
    copywrite = RichTextField(null=True, blank=True)
    harga = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    pengajar = models.ForeignKey(Pengajar, on_delete=models.CASCADE, null=True, blank=True)
    hidden = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    frontpage = models.BooleanField(default=False)
    playlist = models.BooleanField(default=False)
    ytb_playlist_url = models.CharField(max_length=300, null=True, blank=True)
    password = models.CharField(max_length=20, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id) + "-" + self.judul

class Tugas(models.Model):
    judul = models.CharField(max_length=25)
    kode = models.CharField(max_length=10, null=True, blank=True)
    deskripsi = models.TextField()
    nilai_max = models.IntegerField(default=100)

    def __str__(self):
        return str(self.id) + "-" + self.judul

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
    isi_tambahan = RichTextField(null=True, blank=True)
    tugas = models.ForeignKey(Tugas, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + str("-") + str(self.materi) + str("-") + str(self.no_urut) + str("-") + str(self.judul)

    
class Pengumuman(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    judul = models.CharField(max_length=100,null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    isi = RichTextField()
    display = models.BooleanField(default=False)
    frontpage = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    msg_content = models.TextField()
    url = models.CharField(max_length=200, null=True, blank=True)
    readed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    @classmethod
    def create_msg(cls, sender, receiver, msg_content, readed):
        sender = User.objects.get(username=sender)
        receiver = User.objects.get(username=receiver)
        message = cls(sender=sender, receiver=receiver, msg_content=msg_content, readed=readed)
        return message

    def __str__(self):
        return self.sender.username + "-" + self.receiver.username


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
    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE )
    no_urut = models.IntegerField()
    tipe = models.CharField(max_length=20, choices=TIPE)
    judul = models.CharField(max_length=25)
    pertanyaan = models.TextField()
    penjelasan = models.TextField()
    benarsalah = models.BooleanField(null=True, blank=True)
    multianswer = models.BooleanField(null=True, blank=True, default=False)
    tags = models.ManyToManyField(TagSoal, blank=True)
    jawaban_url = models.CharField(max_length=100, null=True, blank=True)
    jawaban_essay = RichTextField(null=True, blank=True)
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
    status = models.CharField(max_length=20, choices=STATUS, default='posted')

    @classmethod
    def daftar(cls, user, materi, harga):
        user = User.objects.get(username=user)
        materi = Materi.objects.get(id=materi)
        no_order = random_char(5).upper()
        pembayaran = cls(user=user, materi=materi, no_order=no_order, harga=harga)
        return pembayaran

    def __str__(self):
        return self.no_order + "-" + self.user.username + "-" + self.materi.judul + ":" + self.status

class Pendaftaran(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE)

    @classmethod
    def daftar(cls, user, materi):
        user = User.objects.get(username=user)
        materi = Materi.objects.get(id=materi)
        pendaftaran = cls(user=user, materi=materi)
        return pendaftaran

    def __str__(self):
        return self.user.username + " - " + self.materi.judul

class Favorit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.materi.judul


class Jawaban(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE)
    soal = models.ForeignKey(Soal, on_delete=models.CASCADE)
    jawaban = models.TextField(null=True, blank=True)
    nilai = models.IntegerField(default=0)
    check = models.BooleanField(default=False)

    @classmethod
    def berinilai(cls, user, topic, tugas, soal, jawaban, nilai, check):

        #check first
        user = User.objects.get(username=user)
        topic = Topic.objects.get(id=topic)
        tugas = Tugas.objects.get(id=tugas)
        soal = Soal.objects.get(id=soal)

        check_ = Jawaban.objects.filter(user=user.id)
        check_ = check_.filter(topic=topic.id)
        check_ = check_.filter(tugas=tugas.id)
        check_ = check_.filter(soal=soal.id)
        
        if not check_:
            nilai = cls(user=user, topic=topic,tugas=tugas, soal=soal, jawaban=jawaban, nilai=nilai, check=check)
        else:
            check_.delete()
            nilai = cls(user=user, topic=topic,tugas=tugas, soal=soal, jawaban=jawaban, nilai=nilai, check=check)

        return nilai

    def __str__(self):
        return str(self.id) + "-" + self.user.username + "-" + str(self.soal.id) + "-" + self.soal.pertanyaan

    
class Logakses(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    soal = models.ForeignKey(Soal, on_delete=models.CASCADE, null=True, blank=True)
    keterangan = models.CharField(max_length=100, null=True, blank=True)
    api = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id) + "-" + self.user.username + "-" + self.keterangan + "-" + str(self.date_created)
    
class Review(models.Model):
    bintang = (
        (1,'*'),
        (2,'**'),
        (3,'***'),
        (4,'****'),
        (5,'*****')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE, null=True, blank=True)
    ulasan = RichTextField()
    rating = models.IntegerField(default='5', choices=bintang)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id) + "-" + self.user.username + "-[" + self.materi.judul + "]-" + str(self.ulasan) + "-" + str(self.rating)

class Penyelenggara(models.Model):
    statusp = (
        ('belum terverifikasi', 'belum terverifikasi'),
        ('terverifikasi', 'terverifikasi'),
        ('pending', 'pending'),
    )
    nama_penyelenggara = models.CharField(max_length=200, null=True)
    alamat_penyelenggara = models.TextField()
    status = models.CharField(max_length=50, choices=statusp)
    def __str__(self):
        return str(self.id) + "-" + self.nama_penyelenggara

class Kegiatan(models.Model):
    bintang = (
        (1,'*'),
        (2,'**'),
        (3,'***'),
        (4,'****'),
        (5,'*****')
    )

    status_acr = (
        ('belum terverifikasi', 'belum terverifikasi'),
        ('terverifikasi', 'terverifikasi'),
        ('pending', 'pending')
    )

    judul_acara =  models.CharField(max_length=200, null=True)
    status_acara = models.CharField(max_length=100, choices=status_acr, null=True)
    penyelenggara =  models.ForeignKey(Penyelenggara, on_delete=models.CASCADE, null=True, blank=True)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE, null=True, blank=True)
    deskripsi = RichTextField()
    rating = models.IntegerField(default='5', choices=bintang)
    tanggal_mulai = models.DateTimeField(null=True)
    tanggal_selesai = models.DateTimeField(null=True)
    url_donasi = models.CharField(max_length=300, null=True)

    def __str__(self):
        return str(self.id)+"-"+self.judul_acara


class RingKegiatan(models.Model):
    bintang = (
        (1,'*'),
        (2,'**'),
        (3,'***'),
        (4,'****'),
        (5,'*****')
    )

    status_acr = (
        ('belum terverifikasi', 'belum terverifikasi'),
        ('terverifikasi', 'terverifikasi'),
        ('pending', 'pending')
    )

    ring_ref = models.CharField(max_length=200, null=True, blank=True)
    judul_acara =  models.CharField(max_length=200, null=True)
    status_acara = models.CharField(max_length=100, choices=status_acr, null=True)
    penyelenggara =  models.ForeignKey(Penyelenggara, on_delete=models.CASCADE, null=True, blank=True)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE, null=True, blank=True)
    lokasi = models.CharField(max_length=200,null=True, blank=True)
    deskripsi = RichTextField()
    rating = models.IntegerField(default='5', choices=bintang)
    tanggal_mulai = models.DateTimeField(null=True)
    tanggal_selesai = models.DateTimeField(null=True)
    url_donasi = models.CharField(max_length=300, null=True)

    def __str__(self):
        return str(self.id)+"-"+self.judul_acara


class Ring_getter(models.Model):
    ring_name = models.CharField(max_length=200,null=True, blank=True)
    ring_ref = models.CharField(max_length=200,null=True, blank=True)
    ring_url = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.name)+"-"+self.ring_ref
