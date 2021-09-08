import django_filters

from .models import *

class MateriFilter(django_filters.FilterSet):
    class Meta:
        model = Materi
        fields = ['rating', 'kategori', 'playlist', 'tags']