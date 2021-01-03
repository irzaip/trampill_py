from django.db import models
from django.contrib.auth.models import User
import string, random
from ckeditor.fields import RichTextField


def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))

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
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    copywrite = RichTextField(null=True, blank=True)
    harga = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    pengajar = models.CharField(max_length=40, null=True, blank=True)
    tentang_pengajar = RichTextField(null=True, blank=True)
    hidden = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    frontpage = models.BooleanField(default=False)
    playlist = models.BooleanField(default=False)


    def __str__(self):
        return str(self.id) + "-" + self.judul

class Tugas(models.Model):
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