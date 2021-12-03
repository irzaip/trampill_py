import requests
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
from .future import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import *
import json
from decimal import Decimal

@api_view(['POST'])
@permission_classes([IsAdminUser])
def reconnect_server(request):
    server = json.dumps(request.data)
    with open("blockserver.txt", "w") as f:
        f.write(server)
    return Response(json.loads(server))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_balance(request):

    with open("blockserver.txt") as f:
        url = json.loads(f.read())['url']
    headers = {'content-type': 'application/json'}

    kupon_account = json.loads(json.dumps(request.data))['kupon_account']

    payload = {
        "method": "eth_getBalance",
        "params": [ kupon_account , "latest"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    balance = int(str(json.loads(json.dumps(response))['result']),16) / 1e+18
    return Response(str(balance))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_bytxid(request, txid):
    pass



