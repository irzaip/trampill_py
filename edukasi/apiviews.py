from rest_framework import response
from .models import *
from .mylib import *
from .decorators import *
from .filter import *
from .forms import *
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages as int_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from edukasi.serializers import *
from django.http import JsonResponse
from django.urls import reverse
import pprint
from django.http import HttpResponse


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import make_aware
from django.conf import settings

import random
import ast

from .youtube import *
from .future import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import *
import json
from .views import message_user
from django.utils import timezone
timezone.now

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([AllowAny])
def apiview(request, format=None):
    """
# DAFTAR API di TRAMPILL.com
- [Mengambil daftar materi /api/listmateri](/api/listmateri)
- [Mengambil daftar kegiatan /api/listkegiatan](/api/listkegiatan)
- [Mengambil detail materi /api/materi/(materi_id)](/api/materi/1)
- [Mengambil topik-topik dari materi. -PUBLIK /api/listtopic/(materi_id)](/api/listtopic/1)
- [Mengambil topik-topik dari materi.. /api/topic/(materi_id)](/api/topic/1)
- [Mengambil nama user by id /api/user/(user_id)](/api/user/1)
- [Mengambil message untuk user logged in /api/message](/api/message/)
- [Mengambil daftar materi apa saja yang terdaftar /api/pendaftaran](/api/pendaftaran/)
- [Mendaftar materi berdasarkan idnya /api/mendaftar/(materi_id)](/api/mendaftar/1)
- [Mengambil daftar materi yang di beri tanda favorit /api/favorit/](/api/favorit/)
- [Membuat sebuah materi menjadi favorit /api/buatfavorit/(materi_id)](/api/buatfavorit/1)
- [Melihat seluruh daftar pembayaran /api/pembayaran/](/api/pembayaran)
- [Melihat tugas /api/tugas/(tugas_id)](/api/tugas/1)
- [Melihat soal berdasarkan id /api/soal/(soal_id)](/api/soal/1)
- [Mencatat user apabila sudah melihat sebuah topik_id /api/view_topic/(topic_id)](/api/view_topic/2)
- [Melihat kegiatan berdasarkan id-nya /api/kegiatan/(kegiatan_id)](/api/kegiatan/1)
- [Mendaftar sebagai user baru /api/register](/api/register/)
- [Mengambil quote of the day /api/inspiring](/api/inspiring)
- [Koneksi ulang blockchain /api/reconnect_server](/api/reconnect_server)
- [Mengambil data jumlah Voucher /api/get_balance](/api/get_balance)
- [Mengambil data transaksi voucher berdasarkan id /api/get_bytxid](/api/get_bytxid)
- [Mendapatkan token JWt setelah login /api/token](/api/token)
- [Refresh token JWT setelah 12 Jam /api/token/refresh](/api/token/refresh)
- [Mengambil userprofile yang sedang login /api/userprofile/](/api/userprofile/)
    """
    return Response("done")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topic_apiview(request, pk, format=None):

    check = Pendaftaran.objects.filter(user=request.user, materi=pk)
    if not check:
        return Response({'status': 'Belum terdaftar'})

    try:
        queryset = Topic.objects.filter(materi=pk).order_by('no_urut')
    except:
        return Response({'status': 'Data not exist'})

    serial = TopicSerializer(queryset, many=True)
    Logakses.objects.create(user=request.user, materi=Materi.objects.get(id=pk), keterangan="topiclist", api=True)
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listtopic_apiview(request, pk, format=None):

    try:
        queryset = Topic.objects.filter(materi=pk).order_by('no_urut')
    except:
        return Response({'status': 'Data not exist'})

    serial = ListTopicSerializer(queryset, many=True)
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def materi_apiview(request, pk, format=None):
    try:
        queryset = Materi.objects.get(id=pk)
    except:
        return Response({'status': 'Data not exist'})

    serial = MateriSerializer(queryset, many=False)
    Logakses.objects.create(user=request.user, materi=queryset, keterangan="materi", api=True)
    return Response(serial.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def kegiatan_apiview(request, pk, format=None):
    try:
        queryset = Kegiatan.objects.get(id=pk)
    except:
        return Response({'status': 'Data Not Exists'})

    serial = KegiatanSerializer(queryset, many=False)
    #Logakses.objects.create(user=request.user, keterangan="kegiatan", api=True)
    return Response(serial.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def listmateri_apiview(request, format=None):
    """
type: GET  
permission: AllowAny  

Api ini untuk mengambil Seluruh Listing Materi yang ada di  
trampill.com, semua informasi umum materi terdapat pada json ini.

### settingan penting
- harga : Harga yang harus dibayar untuk mendaftar materi  
- discount : jumlah discount yang berlaku (dalam satuan %)  
- hidden : tidak ditampilkan di halaman pertama
- featured : masuk ke rekomendasi atau unggulan.
- playlist : materi yang terkoneksi dengan playlist youtube / yg lain.
- password : materi yang memerlukan password untuk mendaftar.
- pendek : adalah deskripsi dalam format yang lebih pendek.
- deskripsi : adalah penjelasan umum tentang materi.

    """
    try:
        queryset = Materi.objects.all()
    except:
        return Response({'status': 'Error retrieving'})

    serial = MateriSerializer(queryset, many=True, context={'request': request})
    #Logakses.objects.create(user=request.user, keterangan="listmateri", api=True)
    return Response(serial.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def listkegiatan_apiview(request, format=None):
    try:
        today = datetime.today()
        
        #queryset = Kegiatan.objects.filter(tanggal_mulai__lt=today, tanggal_selesai__gt=today)
        queryset = Kegiatan.objects.all()
        
    except:
        return Response({'status': 'Error retrieving'})

    serial = KegiatanSerializer(queryset, many=True, context={'request': request})
    #Logakses.objects.create(user=request.user, keterangan="listmateri", api=True)
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_apiview(request, format=None):
    queryset = Message.objects.filter(receiver=request.user, readed=False)
    serial = MessageSerializer(queryset, many=True, context={'request': request})
    return Response(serial.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userprofile(request, format=None):
    try:
        queryset = User.objects.get(username=request.user)
        serial = UserProfilSerializer(queryset, many=False, context={'request': request})
        return Response(serial.data)
    except:
        return Response({'status': 'Error get user profile'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_apiview(request, pk):
    try:
        queryset = User.objects.get(id=pk)
    except:
        return Response({'status': 'User error'})
    
    serial = UserDetailSerializer(queryset, many=False)
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pendaftaran_apiview(request):
    queryset = Pendaftaran.objects.filter(user=request.user)
    
    serial = PendaftaranSerializer(queryset, many=True)
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hapuspendaftaran(request, pk):
    try:
        queryset = Pendaftaran.objects.filter(user=request.user, materi=pk)
        print(queryset)
        queryset.delete()
        return Response({"status" : "Materi berhasil dihapus"})
    except:
        return Response({"status" : "Gagal menghapus materi"})




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorit_apiview(request):
    queryset = Favorit.objects.filter(user=request.user)
    
    serial = FavoritSerializer(queryset, many=True)
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pembayaran_apiview(request):
    queryset = Pembayaran.objects.filter(user=request.user)
    
    serial = PembayaranSerializer(queryset, many=True)
    return Response(serial.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mendaftar_apiview(request, pk):

    check = Pendaftaran.objects.filter(user=request.user, materi=pk)
    if not check:
        try:
            checkmateri = Materi.objects.get(id=pk)
            price = checkmateri.harga
            discount = checkmateri.discount
            bayar = (price * (100 - discount)) / 100
            rndm = random.randint(0, 99)
            byr_rnd = bayar + rndm
        except:
            return Response({'status': 'Materi tidak ditemukan'})        

        # if (int(checkmateri.harga) - (int(checkmateri.harga) * int(checkmateri.discount) / 100) > 0):
        #     return Response({'status': 'Harus melakukan pembayaran terlebih dahulu'})
        # else:
        #     daftar = Pendaftaran.objects.create(materi=checkmateri, user=request.user)

        if request.method == "POST":
            pprint.pprint(request.POST.get('password'))
            password = request.POST.get('password')
            if not password:
                password = ""
                print(password.lower())
                print(checkmateri.password.lower())
            if (bayar == 0 and password.lower() == checkmateri.password.lower()):
                pendaftaran = Pendaftaran.daftar(request.user, pk)
                pendaftaran.save()
                message_user(request.user,receiver="staff", message="Daftar Materi baru")
                print("sukses mendaftar")
                return Response({"status": "Sukses, Materi telah di daftarkan"})
            elif (password.lower() != checkmateri.password.lower()):
                #int_messages.error(request, 'Password salah')
                print("mendaftar gagal")
                return Response({"status":"Mendaftarkan Gagal, password salah"})
            else:
                pembayaran = Pembayaran.daftar(request.user, pk, byr_rnd)
                pembayaran.save()
                message_user(request.user, receiver="staff", message="Pembayaran materi", url=reverse("listpembayaran"))
                message_user(sender="admin", receiver=request.user, message="Menunggu pembayaran materi", url=reverse("pembayaran"))
                Logakses.objects.create(user=request.user, materi=Materi.objects.get(id=pk), keterangan="mendaftar", api=True)
                print("mendaftar pending")
                return Response({"status" : "Pendaftaran diterima, untuk Akses silahkan melakukan pembayaran sesuai yang ada di menu PEMBAYARAN."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tugas_apiview(request,pk):

    queryset = Tugas.objects.filter(id=pk)
    
    serial = TugasSerializer(queryset, many=True)
    Logakses.objects.create(user=request.user, keterangan="lihattugas", api=True)
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def soal_apiview(request,pk):
    
    queryset = Soal.objects.filter(tugas=pk)
    
    serial = SoalSerializer(queryset, many=True)
    Logakses.objects.create(user=request.user, keterangan="lihatsoal", api=True)
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_topic(request,pk):
    Logakses.objects.create(user=request.user, topic=Topic.objects.get(id=pk), keterangan="topicview", api=True)
    return Response({"status": "logged"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buatfavorit(request, pk):
    user = User.objects.get(username=request.user)
    try:
        materi = Materi.objects.get(id=pk)
    except:
        return Response({"status":"Gagal, materi salah"})
    check_fav = Favorit.objects.filter(user=user, materi=materi)

    if not check_fav:
        favorit = Favorit(user=user, materi=materi)
        favorit.save()
    else:
        check_fav.delete()

    return Response({"status": "berhasil"})


@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Registrasi berhasil, Aktivasi terlebih dahulu, check email anda!"
            data['email'] = user.email
            data['username'] = user.username

            current_site = get_current_site(request)
            mail_subject = 'Activate your TRAMPILL account.'
            message = render_to_string('edukasi/acc_active_email.html', {
                'user': user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            #context['uidb64'] = urlsafe_base64_encode(force_bytes(user.pk))
            #context['token'] = account_activation_token.make_token(user)

        else:
            data = serializer.errors
        return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def inspiring(request):
    futura = inspirasi()
    return JsonResponse({'response': futura})
