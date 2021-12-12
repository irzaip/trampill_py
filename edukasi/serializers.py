from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.db.models.fields import EmailField
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_pass')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = User(username=self.validated_data['username'],email= self.validated_data['email'])
        password = self.validated_data['password']
        confirm_pass = self.validated_data['confirm_pass']
        user.is_active = False
        if password != confirm_pass:
            raise serializers.ValidationError({'error': 'Password must match'})
        user.set_password(password)
        user.save()
        group = Group.objects.get(name='customer')
        user.groups.add(group)
        return user




class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class MateriSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, read_only=True,slug_field='name')
    pengajar = serializers.ReadOnlyField(source='pengajar.nama')
    tentang_pengajar = serializers.ReadOnlyField(source='pengajar.tentang_pengajar')
    password = serializers.SerializerMethodField()

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
            'password'
        ]

    def get_password(self, instance):
        return (True if instance.password else False)

class KegiatanSerializer(serializers.ModelSerializer):
    pengajar = serializers.ReadOnlyField(source='pengajar.nama')
    tentang_pengajar = serializers.ReadOnlyField(source='pengajar.tentang_pengajar')
    penyelenggara = serializers.ReadOnlyField(source='penyelenggara.')
    judul_materi = serializers.ReadOnlyField(source='materi.judul')

    class Meta:
        model = Kegiatan
        fields = [
            'id',
            'judul_acara',
            'status_acara',
            'penyelenggara',
            'judul_materi',
            'deskripsi',
            'pengajar',
            'tentang_pengajar',
            'rating',
            'tanggal_mulai',
            'tanggal_selesai',
            'url_donasi',
        ]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['materi', 'no_urut', 'judul', 'jenis', 'link', 'isi_tambahan', 'tugas']

class ListTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['materi', 'no_urut', 'judul', 'jenis']

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



class UserExtSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExt
        fields = [
             'user',
             'phone',
             'kota',
             'kupon_account',
             'last_balance',
             'last_balance_created',
             'date_created',
        ]

class UserProfilSerializer(serializers.ModelSerializer):
    #userext = UserExtSerializer(many=False)
    phone = serializers.ReadOnlyField(source='userext.phone')
    kota = serializers.ReadOnlyField(source='userext.kota')
    kupon_account = serializers.ReadOnlyField(source='userext.kupon_account')
    last_balance = serializers.ReadOnlyField(source='userext.last_balance_created')
    date_created = serializers.ReadOnlyField(source='userext.date_created')

    class Meta:
        model = User
        fields = '__all__'
        #depth = 1



class PendaftaranSerializer(serializers.ModelSerializer):
    materi = MateriSerializer(many=False)

    class Meta:
        model = Pendaftaran
        fields = ['materi']
        
class FavoritSerializer(serializers.ModelSerializer):
    materi = MateriSerializer(many=False)
    
    class Meta:
        model = Favorit
        fields = ['materi']

class PembayaranSerializer(serializers.ModelSerializer):
    materi = MateriSerializer(many=False)
    user = UserDetailSerializer(many=False)

    class Meta:
        model = Pembayaran
        fields = [
            'id',
            'harga',
            'date_created',
            'no_order',
            'status',                
            'materi',
            'user',
            ]


        depth = 1

    #def get_password(self, instance):
    #    return (True if instance.password else False)


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

