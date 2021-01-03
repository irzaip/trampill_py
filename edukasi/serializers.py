from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class MateriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materi
        fields = ['judul', 'deskripsi']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['materi', 'no_urut', 'judul', 'jenis', 'link', 'isi_tambahan', 'tugas']

