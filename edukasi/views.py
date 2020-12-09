from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages as int_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from edukasi.serializers import UserSerializer, GroupSerializer

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib.auth.decorators import user_passes_test


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
from .mylib import *


# Create your views here.
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            fullname = str(form.cleaned_data.get('first_name')) + str(form.cleaned_data.get('lastname'))

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            # Customer.objects.create(
            #     user=user,
            # )

            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('edukasi/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()


            int_messages.success(request,"Account created successfully, FIRST verify your EMAIL")
            return redirect('please_verify')
        else:
            return HttpResponse("Error creating new user -> check user and password requirements")

    context = {'form': form}
    return render(request, 'edukasi/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Terima kasih sudah verifikasi, sekarang anda dapat LOGIN menggunakan akun anda.')
    else:
        return HttpResponse('Activasi tidak berhasil!')


def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            int_messages.error(request,'Username or Password INCORRECT!')
            return redirect('login')
    
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

    if topic_content.jenis == 'Link Video':
        ytb_video = get_yt_v(topic_content.link)
    else:
        ytb_video = ""

    #menarik topic apa saja yang sudah pernah dibuka.
    completed = Komplit.objects.filter(user=request.user).order_by('topic')
    if completed:
        completed = [i.topic.id for i in completed]

    # mengisi tabel komplit dengan topic yang sudah pernah di buka        
    topic_komplit = Komplit.objects.filter(topic=sid, user=request.user)
    if not topic_komplit:
        tsid = Topic.objects.get(id=sid)
        addkomplit = Komplit(topic=tsid, user=request.user)
        addkomplit.save()

    
    context = {'materi': materi, 'topics': topics, 'topic_content': topic_content, 'sid': sid,
        'next': next, 'prev': prev, 'ytb_video': ytb_video, 'completed': completed}
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

def please_verify(request):
    context = {}
    return render(request, 'edukasi/please_verify.html', context)

def messages(request):
    inbox = Message.objects.filter(reciever=request.user)
    sentbox = Message.objects.filter(sender=request.user)

    context = {'inbox': inbox, 'sentbox': sentbox}
    return render(request, 'edukasi/messages.html', context)

@user_passes_test(lambda u: u.is_superuser)
def add_materi(request):
    materi = MateriForm()
    if request.method == "POST":
        materi = MateriForm(request.POST)
        if materi.is_valid():
            mt = materi.save(request.POST)
            return redirect('add_materi_topic', mt.id)

    context = {'materi': materi}
    return render(request, 'edukasi/add_materi.html', context)

@user_passes_test(lambda u: u.is_superuser)
def add_materi_topic(request, sid):
    m_topic = Topic.objects.filter(materi=sid).order_by('no_urut')
    form = TopicForm(initial={'materi': sid})
    

    if request.method == "POST":
        form = TopicForm(request.POST)
        form.id = sid
        if form.is_valid():
            topic = form.save(request.POST)
            return redirect('add_materi_topic', sid)


    context = {'form': form, 'm_topic': m_topic}
    return render(request, 'edukasi/add_materi2.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edit_materi(request,sid):
    instance = Materi.objects.get(id=sid)
    materi = MateriForm(instance=instance)
    materi_id = sid
    context = {'materi': materi, 'materi_id': materi_id}
    if request.method == "POST":
        materi = MateriForm(request.POST, instance=instance)
        if materi.is_valid():
            tt = materi.save()
            return redirect('materi', materi_id)

    return render(request, 'edukasi/add_materi.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edittopic(request,sid):
    instance = Topic.objects.get(id=sid)
    topic = TopicForm(instance=instance)
    context = {'topic': topic}
    if request.method == "POST":
        topic = TopicForm(request.POST, instance=instance)
        if topic.is_valid():
            tt = topic.save()
            return redirect('add_materi_topic', tt.materi.id)

    return render(request, 'edukasi/edittopic.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deltopic(request, sid):
    instance = Topic.objects.get(id=sid)
    materi_id = instance.materi.id
    topic = TopicForm(instance=instance)
    context = {'topic': topic}

    if request.method == "POST":
        topic = TopicForm(request.POST, instance=instance)
        if topic.is_valid():
            tt = instance.delete()
            return redirect('add_materi_topic', materi_id)
    return render(request, 'edukasi/deltopic.html', context)




def listujian(request):
    listujian = Ujian.objects.all()
    
    context = {'listujian': listujian}
    return render(request, 'edukasi/listujian.html', context)

def addujian(request):
    ujian = UjianForm()

    if request.method=="POST":
        ujian = UjianForm(request.POST)
        if ujian.is_valid():
            ujian.save()
            return redirect('listujian')

    context = {'ujian': ujian}
    return render(request, 'edukasi/addujian.html', context)

def editujian(request,sid):
    instance = Ujian.objects.get(id=sid)
    ujianform = UjianForm(instance=instance)
    if request.method == "POST":
        ujianform = UjianForm(request.POST,instance=instance)
        if ujianform.is_valid():
            ujianform.save()

    context = {'ujianform': ujianform}
    return render(request, 'edukasi/editujian.html', context)

def deleteujian(request, sid):
    instance = Ujian.objects.get(id=sid)
    ujianform = UjianForm(instance=instance)
    if request.method=="POST":
        ujianform = UjianForm(request.POST, instance=instance)
        instance.delete()
        return redirect('listujian')

    context = {'ujianform': ujianform}
    return render(request, 'edukasi/deleteujian.html', context)

def listsoal(request):
    listsoal = Soal.objects.all()
    
    context = {'listsoal': listsoal}
    return render(request, 'edukasi/listsoal.html', context)

def addsoal(request):
    soal = SoalForm()
    
    if request.method=="POST":
        soal = SoalForm(request.POST)
        if soal.is_valid():
            soal.save()
            return redirect('listsoal')

    context = {'soal': soal}
    return render(request, 'edukasi/addsoal.html', context)

def editsoal(request,sid):
    instance = Soal.objects.get(id=sid)
    soalform = SoalForm(instance=instance)
    if request.method == "POST":
        soalform = SoalForm(request.POST,instance=instance)
        if soalform.is_valid():
            soalform.save()

    context = {'soalform': soalform}
    return render(request, 'edukasi/editsoal.html', context)

def deletesoal(request, sid):
    instance = Soal.objects.get(id=sid)
    soalform = SoalForm(instance=instance)
    if request.method=="POST":
        soalform = UjianForm(request.POST, instance=instance)
        instance.delete()
        return redirect('listsoal')

    context = {'soalform': soalform}
    return render(request, 'edukasi/deletesoal.html', context)
