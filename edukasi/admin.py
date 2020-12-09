from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserExt)
admin.site.register(Tag)
admin.site.register(Materi)
admin.site.register(Topic)
admin.site.register(Pengumuman)
admin.site.register(Message)
admin.site.register(Ujian)
admin.site.register(TagSoal)
admin.site.register(Soal)
admin.site.register(Komplit)