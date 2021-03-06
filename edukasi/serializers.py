from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.is_active = False
        user.save()
        return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class MateriSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, read_only=True,slug_field='name')

    class Meta:
        model = Materi
        fields = [
            'id',
            'judul',
            'kode',
            'rating',
            'pendek',
            'deskripsi',
            'gambar',
            'kategori',
            'copywrite',
            'tags',
            'harga',
            'discount',
            'pengajar',
            'tentang_pengajar',
            'hidden',
            'featured',
            'frontpage',
            'playlist',
        ]


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
    #materi = MateriSerializer(many=False)
    
    class Meta:
        model = Pendaftaran
        fields = ['materi']
        depth = 1

class FavoritSerializer(serializers.ModelSerializer):
    materi = MateriSerializer(many=False)
    class Meta:
        model = Favorit
        fields = ['user', 'materi']

class PembayaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pembayaran
        fields = ['no_order', 'harga','materi', 'status']
        depth = 1

class TugasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tugas
        fields = ['judul', 'kode','deskripsi', 'nilai_max']
        depth = 1

class SoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soal
        fields = [
          'tugas',
          'no_urut',
          'tipe',
          'judul',
          'pertanyaan',
          'penjelasan',
          'benarsalah',
          'multianswer',
          'tags',
          'jawaban_url',
          'jawaban_essay',
          'jawaban_a',
          'jawaban_b',
          'jawaban_c',
          'jawaban_d',
          'jawaban_e',
          'jawaban_f',
          'jawaban_g',
          'jawaban_h', 
          'jawaban_1',
          'jawaban_2',
          'jawaban_3',
          'jawaban_4',
          'jawaban_5',
          'jawaban_6',
          'jawaban_7',
          'jawaban_8',
        ]
        depth = 1
