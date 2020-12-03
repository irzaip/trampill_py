from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from edukasi.serializers import UserSerializer, GroupSerializer


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

from .models import *
from .forms import *
from .filter import *
from .decorators import *


# Create your views here.
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            fullname = str(form.cleaned_data.get('first_name')) + str(form.cleaned_data.get('lastname'))

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            # Customer.objects.create(
            #     user=user,
            # )
            messages.success(request,"Account created successfully")
            return redirect('login')
        else:
            return HttpResponse("Error creating new user -> check user and password requirements")

    context = {'form': form}
    return render(request, 'edukasi/register.html', context)



def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request,'Username or Password INCORRECT!')

    
    context = {}
    return render(request, 'edukasi/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')


def homePage(request):
    materis = Materi.objects.all()
    context = {'materis': materis}
    return render(request, 'edukasi/home.html', context)

@login_required(login_url='login')
def listmateri(request):
    materis = Materi.objects.all()
    context = {'materis': materis}
    return render(request, 'edukasi/listmateri.html', context)

def materi(request, sid):
    materi = Materi.objects.get(id=sid)
    starttopic = Topic.objects.filter(materi=materi.id).first().id

    try:
        tags = ", ".join([i[1] for i in materi.tags.values_list()])
    except:
        tags = ""

    context = {'materi': materi, 'starttopic': starttopic, 'tags': tags}
    return render(request, 'edukasi/materi.html', context)

@login_required(login_url='login')
def edittopic(request):
    context = {}
    return render(request, 'edukasi/edittopic.html', context)

def topic(request, sid):
    try:
        sid = int(sid)
    except:
        sid = 0
    topic_content = Topic.objects.get(id=sid)
    materi = Materi.objects.get(id=topic_content.materi.id)
    topics = Topic.objects.filter(materi=materi.id).order_by("no_urut")

    #HITUNG TOPIC SEBELUM DAN SESUDAH
    sequence_topics = [i.id for i in topics]
    sidindex = sequence_topics.index(sid)
    if sidindex == 0 and len(sequence_topics) == 1:
        next = 0
        prev = 0
    elif sidindex == 0 and len(sequence_topics) > 0:
        next = sequence_topics[1]
        prev = 0
    elif sidindex == len(sequence_topics) - 1:
        next = 0
        prev = sequence_topics[sidindex-1]
    else:
        next = sequence_topics[sidindex+1]
        prev = sequence_topics[sidindex-1]

    context = {'materi': materi, 'topics': topics, 'topic_content': topic_content, 'sid': sid,
        'next': next, 'prev': prev}
    return render(request, 'edukasi/topic.html', context)

def kontribusi(request):
    context = {}
    return render(request, 'edukasi/kontribusi.html', context)

def faq(request):
    context = {}
    return render(request, 'edukasi/faq.html',context)
    
def feature(request):
    context = {}
    return render(request, 'edukasi/feature.html',context)
