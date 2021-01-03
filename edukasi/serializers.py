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

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'msg_content', 'created_at']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']

class PendaftaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pendaftaran
        fields = ['user', 'materi']

class FavoritSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorit
        fields = ['user', 'materi']

class PembayaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pembayaran
        fields = ['no_order', 'harga','materi', 'status']
        depth = 1
