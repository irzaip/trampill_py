from .models import *
from .mylib import *
from .decorators import *
from .filter import *
from .forms import *
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

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib.auth.decorators import user_passes_test
import random
import ast

from .youtube import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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



class MateriViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Materi.objects.all()
    serializer_class = MateriSerializer
    permission_classes = [permissions.IsAuthenticated]


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
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def materi_apiview(request, pk, format=None):
    try:
        queryset = Materi.objects.get(id=pk)
    except:
        return Response({'status': 'Data not exist'})

    serial = MateriSerializer(queryset, many=False)
    return Response(serial.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_apiview(request, format=None):
    queryset = Message.objects.filter(receiver=request.user, readed=False)
    serial = MessageSerializer(queryset, many=True, context={'request': request})
    return Response(serial.data)

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mendaftar_apiview(request, pk):
    check = Pendaftaran.objects.filter(user=request.user, materi=pk)
    if not check:
        try:
            checkmateri = Materi.objects.get(id=pk)
        except:
            return Response({'status': 'Materi tidak ditemukan'})        
            
        if (int(checkmateri.harga) - (int(checkmateri.harga) * int(checkmateri.discount) / 100) > 0):
            return Response({'status': 'Harus melakukan pembayaran terlebih dahulu'})
        else:

            daftar = Pendaftaran.objects.create(materi=checkmateri, user=request.user)
            

    queryset = Pendaftaran.objects.filter(user=request.user)
    
    serial = PendaftaranSerializer(queryset, many=True)
    return Response(serial.data)

    


    
    serial = PendaftaranSerializer(queryset, many=True)
    return Response(serial.data)
