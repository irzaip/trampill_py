from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserExt)
admin.site.register(Tag)
admin.site.register(Materi)
admin.site.register(Topic)
