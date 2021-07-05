from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserExt)
admin.site.register(Tag)
admin.site.register(Materi)
admin.site.register(Topic)
admin.site.register(Pengumuman)
admin.site.register(Message)
admin.site.register(Tugas)
admin.site.register(TagSoal)
admin.site.register(Soal)
admin.site.register(Komplit)
admin.site.register(Diskusi)
admin.site.register(Pembayaran)
admin.site.register(Pendaftaran)
admin.site.register(Favorit)
admin.site.register(Jawaban)
admin.site.register(Logakses)
admin.site.register(Review)
admin.site.register(Penyelenggara)
admin.site.register(Kegiatan)
admin.site.register(Pengajar)