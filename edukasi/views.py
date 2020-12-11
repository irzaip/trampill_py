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



def get_user_menu(request):
    try:
        pendaftaran = Pendaftaran.objects.filter(user=request.user)
        favorit = Favorit.objects.filter(user=request.user)
    except:
        pendaftaran = None
        favorit = None

    navmenu = {'pendaftaran': pendaftaran, 'favorit': favorit}
    return navmenu

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
    navmenu = get_user_menu(request)

    materis = Materi.objects.all()
    context = {'materis': materis}
    context = {**context, **navmenu}
    return render(request, 'edukasi/home.html', context)


def listmateri(request):
    navmenu = get_user_menu(request)
    materis = Materi.objects.all()
    context = {'materis': materis}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listmateri.html', context)

def materi(request, sid):
    navmenu = get_user_menu(request)
    materi = Materi.objects.get(id=sid)
    starttopic = Topic.objects.filter(materi=materi.id).first().id

    try:
        tags = ", ".join([i[1] for i in materi.tags.values_list()])
    except:
        tags = ""

    context = {'materi': materi, 'starttopic': starttopic, 'tags': tags}
    context = {**context, **navmenu}
    return render(request, 'edukasi/materi.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edittopic(request):
    navmenu = get_user_menu(request)
    context = {}
    context = {**context, **navmenu}
    return render(request, 'edukasi/edittopic.html', context)

@login_required(login_url='login')
def topic(request, sid):
    navmenu = get_user_menu(request)

    try:
        sid = int(sid)
    except:
        sid = 0

    topic_content = Topic.objects.get(id=sid)
    materi = Materi.objects.get(id=topic_content.materi.id)
    pendaftaran = Pendaftaran.objects.filter(user=request.user)
    materi_terdaftar = [p.materi.id for p in pendaftaran]
    
    if materi.id not in materi_terdaftar:
        return redirect('daftarmateri', materi.id)

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

    diskusi = Diskusi.objects.filter(topic=sid)
    diskusiForm = DiskusiForm()
    if request.method == "POST":

        data = {'user': request.user,
                'topic': sid,
                'pesan': request.POST.get('pesan')
                }
        diskusi = DiskusiForm(data)

        if diskusi.is_valid():
            diskusi.save()
            return redirect('topic', sid)
    
    else:
        diskusiForm=DiskusiForm()
    

    context = {'materi': materi, 'topics': topics, 'topic_content': topic_content, 'sid': sid,
        'next': next, 'prev': prev, 'ytb_video': ytb_video, 'completed': completed, 'diskusi': diskusi,
        'diskusiForm': diskusiForm, 'materi_terdaftar': materi_terdaftar
        }
    context = {**context, **navmenu}
    return render(request, 'edukasi/topic.html', context)

def kontribusi(request):
    navmenu = get_user_menu(request)
    context = {}
    context = {**context, **navmenu}
    return render(request, 'edukasi/kontribusi.html', context)

def faq(request):
    navmenu = get_user_menu(request)
    context = {}
    context = {**context, **navmenu}
    return render(request, 'edukasi/faq.html',context)
    
def feature(request):
    navmenu = get_user_menu(request)
    context = {}
    context = {**context, **navmenu}
    return render(request, 'edukasi/feature.html',context)

def please_verify(request):
    navmenu = get_user_menu(request)
    context = {}
    context = {**context, **navmenu}
    return render(request, 'edukasi/please_verify.html', context)

def messages(request):
    navmenu = get_user_menu(request)
    inbox = Message.objects.filter(reciever=request.user)
    sentbox = Message.objects.filter(sender=request.user)

    context = {'inbox': inbox, 'sentbox': sentbox}
    context = {**context, **navmenu}
    return render(request, 'edukasi/messages.html', context)

@user_passes_test(lambda u: u.is_superuser)
def add_materi(request):
    navmenu = get_user_menu(request)
    materi = MateriForm()
    if request.method == "POST":
        materi = MateriForm(request.POST)
        if materi.is_valid():
            mt = materi.save(request.POST)
            return redirect('add_materi_topic', mt.id)

    context = {'materi': materi}
    context = {**context, **navmenu}
    return render(request, 'edukasi/add_materi.html', context)

@user_passes_test(lambda u: u.is_superuser)
def add_materi_topic(request, sid):
    navmenu = get_user_menu(request)
    m_topic = Topic.objects.filter(materi=sid).order_by('no_urut')
    form = TopicForm(initial={'materi': sid})
    

    if request.method == "POST":
        form = TopicForm(request.POST)
        form.id = sid
        if form.is_valid():
            topic = form.save(request.POST)
            return redirect('add_materi_topic', sid)


    context = {'form': form, 'm_topic': m_topic}
    context = {**context, **navmenu}
    return render(request, 'edukasi/add_materi2.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edit_materi(request,sid):
    navmenu = get_user_menu(request)
    instance = Materi.objects.get(id=sid)
    materi = MateriForm(instance=instance)
    materi_id = sid

    if request.method == "POST":
        materi = MateriForm(request.POST, instance=instance)
        if materi.is_valid():
            tt = materi.save()
            return redirect('materi', materi_id)

    context = {'materi': materi, 'materi_id': materi_id}
    context = {**context, **navmenu}
    return render(request, 'edukasi/add_materi.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edittopic(request,sid):
    navmenu = get_user_menu(request)
    instance = Topic.objects.get(id=sid)
    topic = TopicForm(instance=instance)

    if request.method == "POST":
        topic = TopicForm(request.POST, instance=instance)
        if topic.is_valid():
            tt = topic.save()
            return redirect('add_materi_topic', tt.materi.id)

    context = {'topic': topic}
    context = {**context, **navmenu}
    return render(request, 'edukasi/edittopic.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deltopic(request, sid):
    navmenu = get_user_menu(request)
    instance = Topic.objects.get(id=sid)
    materi_id = instance.materi.id
    topic = TopicForm(instance=instance)

    if request.method == "POST":
        topic = TopicForm(request.POST, instance=instance)
        if topic.is_valid():
            tt = instance.delete()
            return redirect('add_materi_topic', materi_id)

    context = {'topic': topic}
    context = {**context, **navmenu}
    return render(request, 'edukasi/deltopic.html', context)



@user_passes_test(lambda u: u.is_superuser)
def listujian(request):
    navmenu = get_user_menu(request)
    listujian = Ujian.objects.all()
    
    context = {'listujian': listujian}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listujian.html', context)

@user_passes_test(lambda u: u.is_superuser)
def addujian(request):
    navmenu = get_user_menu(request)
    ujian = UjianForm()

    if request.method=="POST":
        ujian = UjianForm(request.POST)
        if ujian.is_valid():
            ujian.save()
            return redirect('listujian')

    context = {'ujian': ujian}
    context = {**context, **navmenu}
    return render(request, 'edukasi/addujian.html', context)

@user_passes_test(lambda u: u.is_superuser)
def editujian(request,sid):
    navmenu = get_user_menu(request)
    instance = Ujian.objects.get(id=sid)
    ujianform = UjianForm(instance=instance)
    if request.method == "POST":
        ujianform = UjianForm(request.POST,instance=instance)
        if ujianform.is_valid():
            ujianform.save()

    context = {'ujianform': ujianform}
    context = {**context, **navmenu}
    return render(request, 'edukasi/editujian.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deleteujian(request, sid):
    navmenu = get_user_menu(request)
    instance = Ujian.objects.get(id=sid)
    ujianform = UjianForm(instance=instance)
    if request.method=="POST":
        ujianform = UjianForm(request.POST, instance=instance)
        instance.delete()
        return redirect('listujian')

    context = {'ujianform': ujianform}
    context = {**context, **navmenu}
    return render(request, 'edukasi/deleteujian.html', context)

@user_passes_test(lambda u: u.is_superuser)
def listsoal(request):
    navmenu = get_user_menu(request)
    listsoal = Soal.objects.all()
    
    context = {'listsoal': listsoal}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listsoal.html', context)

@user_passes_test(lambda u: u.is_superuser)
def addsoal(request):
    navmenu = get_user_menu(request)
    soal = SoalForm()
    
    if request.method=="POST":
        soal = SoalForm(request.POST)
        if soal.is_valid():
            soal.save()
            return redirect('listsoal')

    context = {'soal': soal}
    context = {**context, **navmenu}
    return render(request, 'edukasi/addsoal.html', context)

@user_passes_test(lambda u: u.is_superuser)
def editsoal(request,sid):
    navmenu = get_user_menu(request)
    instance = Soal.objects.get(id=sid)
    soalform = SoalForm(instance=instance)

    if request.method == "POST":
        soalform = SoalForm(request.POST,instance=instance)
        if soalform.is_valid():
            soalform.save()

    context = {'soalform': soalform}
    context = {**context, **navmenu}
    return render(request, 'edukasi/editsoal.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deletesoal(request, sid):
    navmenu = get_user_menu(request)
    instance = Soal.objects.get(id=sid)
    soalform = SoalForm(instance=instance)
    if request.method=="POST":
        soalform = UjianForm(request.POST, instance=instance)
        instance.delete()
        return redirect('listsoal')

    context = {'soalform': soalform}
    context = {**context, **navmenu}
    return render(request, 'edukasi/deletesoal.html', context)

def materisaya(request):
    navmenu = get_user_menu(request)
    context = {}
    context = {**context, **navmenu}
    return render(request, 'edukasi/materisaya.html', context)

@user_passes_test(lambda u: u.is_superuser)
def listdiskusi(request):
    navmenu = get_user_menu(request)
    listdiskusi = Diskusi.objects.all()
    context = {'listdiskusi': listdiskusi}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listdiskusi.html', context)

@user_passes_test(lambda u: u.is_superuser)
def editdiskusi(request, sid):
    navmenu = get_user_menu(request)
    instance = Diskusi.objects.get(id=sid)
    diskusiForm = DiskusiForm(instance=instance)

    if request.method == "POST":
        diskusiForm = DiskusiForm(request.POST, instance=instance)
        if diskusiForm.is_valid():
            diskusiForm.save()
            return redirect('listdiskusi')

    context = {'diskusiForm': diskusiForm}
    context = {**context, **navmenu}
    return render(request, 'edukasi/editdiskusi.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deletediskusi(request, sid):
    navmenu = get_user_menu(request)
    instance = Diskusi.objects.get(id=sid)
    diskusiForm = DiskusiForm(instance=instance)

    if request.method == "POST":
        diskusiForm = DiskusiForm(request.POST, instance=instance)
        instance.delete()
        return redirect('listdiskusi')

    context = {'diskusiForm': diskusiForm}
    context = {**context, **navmenu}
    return render(request, 'edukasi/deletediskusi.html', context)

@login_required(login_url='login')
def daftarmateri(request, sid):
    navmenu = get_user_menu(request)

    materi = Materi.objects.get(id=sid)
    price = materi.harga

    if request.method == "POST":
        if price == 0:
            pendaftaran = Pendaftaran.daftar(request.user, sid)
            pendaftaran.save()
            return redirect('materi',sid)
        else:
            pembayaran = Pembayaran.daftar(request.user, sid, price)
            pembayaran.save()
            return redirect('home')

    context={'materi': materi, 'price': price}
    context = {**context, **navmenu}

    return render(request, 'edukasi/daftarmateri.html', context)

@login_required(login_url='login')
def favorit(request, sid):
    user = User.objects.get(username=request.user)
    materi = Materi.objects.get(id=sid)
    check_fav = Favorit.objects.filter(user=user, materi=materi)
    
    if not check_fav:
        favorit = Favorit(user=user, materi=materi)
        favorit.save()
    else:
        check_fav.delete()

    return redirect(request.META.get('HTTP_REFERER'))
