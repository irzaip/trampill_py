from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm,  PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages as int_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from edukasi.serializers import *
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.template.context_processors import csrf
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .youtube import *
from .models import *
from .mylib import *
from .decorators import *
from .filter import *
from .forms import *
from .tokens import account_activation_token
from .future import *
from crispy_forms.utils import render_crispy_form
import random
import ast



def message_user(sender, receiver, message, url=None):
    sender=User.objects.get(username=sender)
    
    if receiver=="superuser":
        receiver=User.objects.filter(is_superuser=True)
        for r in receiver:
            Message.objects.create(sender=sender, receiver=r, msg_content=message, url=url)
    elif receiver == "staff":
        receiver=User.objects.filter(is_staff=True)
        for r in receiver:
            Message.objects.create(sender=sender, receiver=r, msg_content=message, url=url)
    else:
        receiver=User.objects.get(username=receiver)
        Message.objects.create(sender=sender, receiver=receiver, msg_content=message, url=url)


def logthis(user, materi, topic, soal, keterangan):
    Logakses.objects.create(user=user, materi=materi, topic=topic, soal=soal, keterangan=keterangan)

def get_user_menu(request):
    try:
        pendaftaran = Pendaftaran.objects.filter(user=request.user)
        favorit = Favorit.objects.filter(user=request.user)
        pesan = Message.objects.filter(receiver=request.user, readed=False)
    except:
        pendaftaran = None
        favorit = None
        pesan = None

    navmenu = {'pendaftaran': pendaftaran, 'favorit': favorit, 'pesan': pesan}
    return navmenu


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Permohonan reset Password"
					email_template_name = "edukasi/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'neo.trampill.com',
					'site_name': 'Trampill',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'noreply@trampill.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="edukasi/password_reset.html", context={"password_reset_form":password_reset_form})

# Create your views here.
def register_page(request):
    context = dict()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            fullname = str(form.cleaned_data.get('first_name')) + \
                str(form.cleaned_data.get('lastname'))

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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            context['uidb64'] = urlsafe_base64_encode(force_bytes(user.pk))
            context['token'] = account_activation_token.make_token(user)

            int_messages.success(
                request, "Account created successfully, FIRST verify your EMAIL")
            return redirect('please_verify')
        else:
            return HttpResponse("Error creating new user -> check user and password requirements")

    context['form'] = form
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

        message_user(request.user, receiver="superuser", message="New User")
        return HttpResponse('Terima kasih sudah verifikasi, sekarang anda dapat LOGIN menggunakan akun anda.')
    else:
        return HttpResponse('Aktivasi tidak berhasil!')


def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            int_messages.error(request, 'Username or Password INCORRECT!')
            return redirect('login')

    context = {}
    return render(request, 'edukasi/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


def home_page(request):
    navmenu = get_user_menu(request)

    import datetime
    today = datetime.datetime.today()
    kegiatans = Kegiatan.objects.filter(tanggal_mulai__lt=today, tanggal_selesai__gt=today)

    materis = Materi.objects.order_by('-created_at')[:4]

    featured = Materi.objects.filter(featured=True)[:4]

    playlist = Materi.objects.order_by('-created_at').filter(playlist=True)

    pengumuman = Pengumuman.objects.filter(frontpage=True)

    _inspirasi = inspirasi()

    context = {'materis': materis, 
        'playlist': playlist, 
        'kegiatans': kegiatans, 
        'pengumuman': pengumuman, 
        'inspirasi': _inspirasi,
        'featured': featured}
    context = {**context, **navmenu}
    
    return render(request, 'edukasi/home.html', context)

@login_required(login_url='login')
def dashboard(request):
    navmenu = get_user_menu(request)

    materis = Pendaftaran.objects.filter(user=request.user)

    if request.user.is_superuser:
        dashboard = [{'judul': 'Total user', 'angka': User.objects.all().count() },
            {'judul': 'Total Materi', 'angka': Materi.objects.all().count()},
            {'judul': 'Total Tugas', 'angka': Tugas.objects.all().count()},
            {'judul': 'Total Soal', 'angka': Soal.objects.all().count()},
        ]
    else:
        dashboard = {}
        
    context = {'materis': materis, 'dashboard': dashboard}
    context = {**context, **navmenu}
    return render(request, 'edukasi/dashboard.html', context)


def listmateri(request):
    navmenu = get_user_menu(request)
    materis = Materi.objects.filter()

    mFilter = MateriFilter(request.GET, queryset=materis)
    materis = mFilter.qs

    if request.user.is_authenticated:
        logthis(request.user, None , None, None, "browse listmateri")

    context = {'materis': materis, 'mFilter': mFilter}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listmateri.html', context)

def searchmateri(request):
    ss = request.GET.get("ss")
    if not ss:
        ss = ""
    navmenu = get_user_menu(request)
    materis = Materi.objects.filter(judul__icontains=str(ss))
#    materis2 = Materi.objects.filter(deskripsi__icontains=str(ss))
#    materis = materis.append(materis2)

    mFilter = MateriFilter(request.GET, queryset=materis)
    materis = mFilter.qs

    if request.user.is_authenticated:
        logthis(request.user, None , None, None, "browse listmateri")

    context = {'materis': materis, 'mFilter': mFilter}
    context = {**context, **navmenu}
    return render(request, 'edukasi/searchmateri.html', context)

def listplaylist(request):
    navmenu = get_user_menu(request)
    materis = Materi.objects.filter(playlist=True)

    mFilter = MateriFilter(request.GET, queryset=materis)
    materis = mFilter.qs

    if request.user.is_authenticated:
        logthis(request.user, None , None, None, "browse listplaylist")

    context = {'materis': materis, 'mFilter': mFilter}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listplaylist.html', context)


def materi(request, sid):
    navmenu = get_user_menu(request)
    materi = Materi.objects.get(id=sid)
    starttopic = Topic.objects.filter(materi=materi.id).first().id

    try:
        tags = ", ".join([i[1] for i in materi.tags.values_list()])
    except:
        tags = ""

    topics = Topic.objects.filter(materi=materi.id)

    review = Review.objects.filter(materi=materi.id)


    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            ulasan = form.cleaned_data.get('ulasan')
            rating = form.cleaned_data.get('rating')
            form.save()
            print("Saved")
            redirect('materi', sid)
    else:
        data = {'user': request.user, 'materi': sid}
        form = ReviewForm(initial=data)

    if request.user.is_authenticated:
        logthis(request.user, materi=materi, topic=None, soal=None, keterangan="Daftar isi materi")

    context = {'materi': materi, 'starttopic': starttopic,
               'tags': tags, 'topics': topics, 'review': review, 'form': form}
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

    # HITUNG TOPIC SEBELUM DAN SESUDAH
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

    # menarik topic apa saja yang sudah pernah dibuka.
    completed = Komplit.objects.filter(user=request.user).order_by('topic')
    if completed:
        completed = [i.topic.id for i in completed]

    # mengisi tabel komplit dengan topic yang sudah pernah di buka
    topic_komplit = Komplit.objects.filter(topic=sid, user=request.user)
    if not topic_komplit:
        tsid = Topic.objects.get(id=sid)
        addkomplit = Komplit(topic=tsid, user=request.user)
        addkomplit.save()

    if topic_content.tugas:
        tugas = Tugas.objects.get(id=topic_content.tugas.id)
    else:
        tugas = ""

    diskusi = Diskusi.objects.filter(topic=sid)

    if request.method == "POST":
        diskusiForm = DiskusiForm(request.POST)
        if diskusiForm.is_valid():
            pesan = diskusiForm.cleaned_data.get('pesan')
            diskusiForm.save()
            
            message_user(request.user, receiver="staff", message="Diskusi baru", url=reverse("topic", args=[sid]))
            return redirect('topic', sid)
    else:
        data = {'user': request.user,
                'topic': sid, }
        diskusiForm = DiskusiForm(initial=data)

    if request.user.is_authenticated:
        logthis(request.user, materi=materi, topic=topic_content, soal=None, keterangan="Buka topic")

    context = {'materi': materi, 'topics': topics, 'topic_content': topic_content, 'sid': sid,
               'next': next, 'prev': prev, 'ytb_video': ytb_video, 'completed': completed, 'diskusi': diskusi,
               'diskusiForm': diskusiForm, 'materi_terdaftar': materi_terdaftar, 'tugas': tugas
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
    return render(request, 'edukasi/faq.html', context)


def feature(request):
    navmenu = get_user_menu(request)
    context = {}
    context = {**context, **navmenu}
    return render(request, 'edukasi/feature.html', context)


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
def edit_materi(request, sid):
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
def edittopic(request, sid):
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
def listtugas(request):
    navmenu = get_user_menu(request)
    listtugas = Tugas.objects.all()

    context = {'listtugas': listtugas}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listtugas.html', context)


@user_passes_test(lambda u: u.is_superuser)
def addtugas(request):
    navmenu = get_user_menu(request)
    tugas = TugasForm()

    if request.method == "POST":
        tugas = TugasForm(request.POST)
        if tugas.is_valid():
            tugas.save()
            return redirect('listtugas')

    context = {'tugas': tugas}
    context = {**context, **navmenu}
    return render(request, 'edukasi/addtugas.html', context)


@user_passes_test(lambda u: u.is_superuser)
def edittugas(request, sid):
    navmenu = get_user_menu(request)
    instance = Tugas.objects.get(id=sid)
    tugasform = TugasForm(instance=instance)
    if request.method == "POST":
        tugasform = TugasForm(request.POST, instance=instance)
        if tugasform.is_valid():
            tugasform.save()

    context = {'tugasform': tugasform}
    context = {**context, **navmenu}
    return render(request, 'edukasi/edittugas.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deletetugas(request, sid):
    navmenu = get_user_menu(request)
    instance = Tugas.objects.get(id=sid)
    tugasform = TugasForm(instance=instance)
    if request.method == "POST":
        tugasform = TugasForm(request.POST, instance=instance)
        instance.delete()
        return redirect('listtugas')

    context = {'tugasform': tugasform}
    context = {**context, **navmenu}
    return render(request, 'edukasi/deletetugas.html', context)


@user_passes_test(lambda u: u.is_superuser)
def listsoal(request):
    navmenu = get_user_menu(request)
    listsoal = Soal.objects.all()

    context = {'listsoal': listsoal}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listsoal.html', context)


@user_passes_test(lambda u: u.is_superuser)
def addsoal(request, sid):
    navmenu = get_user_menu(request)
    instance = Tugas.objects.get(id=sid)
    soal = SoalForm(initial={'tugas': instance.id})

    all_soal = Soal.objects.filter(tugas=sid)

    if request.method == "POST":
        soal = SoalForm(request.POST, initial={'tugas': instance.id})
        if soal.is_valid():
            soal.save()
            return redirect('listsoal')

    context = {'soal': soal, 'all_soal': all_soal}
    context = {**context, **navmenu}
    return render(request, 'edukasi/addsoal.html', context)


@user_passes_test(lambda u: u.is_superuser)
def editsoal(request, sid):
    navmenu = get_user_menu(request)
    instance = Soal.objects.get(id=sid)
    soalform = SoalForm(instance=instance)

    if request.method == "POST":
        soalform = SoalForm(request.POST, instance=instance)
        if soalform.is_valid():
            soalform.save()
            return redirect('addsoal', instance.tugas.id)

    context = {'soalform': soalform}
    context = {**context, **navmenu}
    return render(request, 'edukasi/editsoal.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deletesoal(request, sid):
    navmenu = get_user_menu(request)
    instance = Soal.objects.get(id=sid)
    soalform = SoalForm(instance=instance)
    if request.method == "POST":
        soalform = SoalForm(request.POST, instance=instance)
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
    discount = materi.discount
    bayar = (price * (100 - discount)) / 100
    rndm = random.randint(0, 99)
    byr_rnd = bayar + rndm

    if request.method == "POST":
        if bayar == 0:
            pendaftaran = Pendaftaran.daftar(request.user, sid)
            pendaftaran.save()
            message_user(request.user,receiver="staff", message="Daftar Materi baru")
            return redirect('materi', sid)
        else:
            pembayaran = Pembayaran.daftar(request.user, sid, byr_rnd)
            pembayaran.save()
            message_user(request.user, receiver="staff", message="Pembayaran materi", url=reverse("pembayaran"))
            return redirect('home')

    context = {'materi': materi, 'price': price, 'discount': discount,
               'bayar': bayar, 'rndm': rndm, 'byr_rnd': byr_rnd}
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

@user_passes_test(lambda u: u.is_superuser)
def listpembayaran(request):
    navmenu = get_user_menu(request)

    listpembayaran = Pembayaran.objects.all().order_by('-date_created')

    context = {'listpembayaran': listpembayaran}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listpembayaran.html', context)

@user_passes_test(lambda u: u.is_superuser)
def setujupembayaran(request, sid):
    pembayaran = Pembayaran.objects.get(id=sid)
    pembayaran.status = 'disetujui'
    pembayaran.save()

    pendaftaran = Pendaftaran.daftar(pembayaran.user, pembayaran.materi.id)
    pendaftaran.save()

    return redirect('listpembayaran')

@user_passes_test(lambda u: u.is_superuser)
def tolakpembayaran(request, sid):
    pembayaran = Pembayaran.objects.get(id=sid)
    pembayaran.status = 'ditolak'
    pembayaran.save()

    return redirect('listpembayaran')

@login_required(login_url='login')
def tugas(request, sid, topic_asal=None):
    navmenu = get_user_menu(request)

    tugas = Tugas.objects.get(id=sid)
    soal = Soal.objects.filter(tugas=sid)
    topic_content = Topic.objects.get(id=request.GET.get("topic_asal"))
    materi = Materi.objects.get(id=topic_content.materi.id)

    pendaftaran = Pendaftaran.objects.filter(user=request.user)
    materi_terdaftar = [p.materi.id for p in pendaftaran]

    topics = Topic.objects.filter(materi=materi.id).order_by("no_urut")

    # HITUNG TOPIC SEBELUM DAN SESUDAH
    sequence_topics = [i.id for i in topics]
    sidindex = sequence_topics.index(topic_content.id)
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

    prevpage = request.META.get('HTTP_REFERER')
    topic_asal = ""

    if request.method == "GET":
        topic_asal = request.GET.get('topic_asal')

    if request.method == "POST":
        soal = request.POST.get('id_idsoal')

    # if returned dan tampilkan info
    info = request.GET.get('info')

    jawaban = Jawaban.objects.filter(
        user=request.user, topic=topic_content.id, tugas=tugas.id)

    context = {'tugas': tugas, 'topic_content': topic_content, 'materi': materi, 'soal': soal,
               'topics': topics, 'prevpage': prevpage, 'topic_asal': topic_asal, 'info': info, 'jawaban': jawaban}
    context = {**context, **navmenu}

    return render(request, 'edukasi/tugas.html', context)

@user_passes_test(lambda u: u.is_superuser)
def periksa(request, sid, topic_asal=None):

    if request.method == "POST":
        idsoal = request.POST.get("id_idsoal")
        soal = Soal.objects.get(id=idsoal)

        topic = Topic.objects.get(id=request.POST.get("topic_asal"))
        tugas = Tugas.objects.get(id=request.POST.get("tugas"))
        materi = Materi.objects.get(id=request.POST.get("materi"))

        if request.user.is_authenticated:
            logthis(request.user, materi=materi, topic=topic, soal=soal, keterangan="Menjawab soal")

        message_user(request.user, "staff", message=str(request.user)+" Menjawab soal")

        if soal.tipe == "Betul / Salah":
            if request.POST.get("id_select") == str(soal.benarsalah):
                # apabila BENAR
                jawab_ = request.POST.get("id_select")
                jawaban = Jawaban.berinilai(
                    request.user, topic.id, tugas.id, soal.id, jawab_, 100, False)
                jawaban.save()

                info = "Jawaban anda benar. " + str(soal.penjelasan)
                url = f"/tugas/{tugas.id}/?topic_asal={topic.id}&materi={materi.id}&info={info}"
                return HttpResponseRedirect(url)
            else:
                jawab_ = request.POST.get("id_select")
                jawaban = Jawaban.berinilai(
                    request.user, topic.id, tugas.id, soal.id, jawab_, 10, False)
                jawaban.save()
                info = "Jawaban anda salah. " + str(soal.penjelasan)
                url = f"/tugas/{tugas.id}/?topic_asal={topic.id}&materi={materi.id}&info={info}"
                return HttpResponseRedirect(url)

        if soal.tipe == "Kumpul URL":
            jawab_ = request.POST.get("id_jawaban_url")
            jawaban = Jawaban.berinilai(
                request.user, topic.id, tugas.id, soal.id, jawab_, 0, True)
            jawaban.save()
            # Send message to admin
            message = Message.create_msg(
                request.user, "admin", "Kumpul URL to be checked", False)
            message.save()

            info = "Postingan tugas anda telah berhasil, admin telah di notifikasi"
            url = f"/tugas/{tugas.id}/?topic_asal={topic.id}&materi={materi.id}&info={info}"
            return HttpResponseRedirect(url)

        if soal.tipe == "Essay":
            jawab_ = request.POST.get("id_jawaban_essay")
            jawaban = Jawaban.berinilai(
                request.user, topic.id, tugas.id, soal.id, jawab_, 0, True)
            jawaban.save()
            # Send message to admin
            message = Message.create_msg(
                request.user, "admin", "Essay to be checked", False)
            message.save()

            info = "Postingan tugas anda telah berhasil, admin telah di notifikasi"
            url = f"/tugas/{tugas.id}/?topic_asal={topic.id}&materi={materi.id}&info={info}"
            return HttpResponseRedirect(url)

        if soal.tipe == "Pilihan Ganda":
            if request.POST.get("id_select") == str(soal.jawaban_1).upper():
                jawab_ = request.POST.get("id_select")
                jawaban = Jawaban.berinilai(
                    request.user, topic.id, tugas.id, soal.id, jawab_, 100, False)
                jawaban.save()
                info = "Jawaban anda benar. " + str(soal.penjelasan)
                url = f"/tugas/{tugas.id}/?topic_asal={topic.id}&materi={materi.id}&info={info}"
                return HttpResponseRedirect(url)
            else:
                jawab_ = request.POST.get("id_select")
                jawaban = Jawaban.berinilai(
                    request.user, topic.id, tugas.id, soal.id, jawab_, 0, False)
                jawaban.save()
                info = "Jawaban anda salah. " + str(soal.penjelasan)
                url = f"/tugas/{tugas.id}/?topic_asal={topic.id}&materi={materi.id}&info={info}"
                return HttpResponseRedirect(url)

    url = f"/tugas/{tugas.id}/?topic_asal={topic.id}&materi={materi.id}"
    return HttpResponseRedirect(url)

@user_passes_test(lambda u: u.is_superuser)
def listjawaban(request):
    navmenu = get_user_menu(request)
    listjawaban = Jawaban.objects.all().order_by('-check')

    context = {'listjawaban': listjawaban}
    context = {**context, **navmenu}

    return render(request, 'edukasi/listjawaban.html', context)

@user_passes_test(lambda u: u.is_superuser)
def editjawaban(request, sid):
    navmenu = get_user_menu(request)
    instance = Jawaban.objects.get(id=sid)
    jawabanForm = JawabanForm(instance=instance)
    if request.method == "POST":
        jawabanForm = JawabanForm(request.POST, instance=instance)
        if jawabanForm.is_valid():
            jawabanForm.save()

            pesan = f"Tugas <<{instance.tugas}-{instance.soal}>> anda telah di nilai."
            message = Message.create_msg("admin", instance.user, pesan, False)
            message.save()

            return redirect('listjawaban')

    context = {'listjawaban': listjawaban, 'jawabanForm': jawabanForm}
    context = {**context, **navmenu}

    return render(request, 'edukasi/editjawaban.html', context)

@login_required(login_url='login')
def readall(request):
    pesan = Message.objects.filter(receiver=request.user, readed=False)
    pesan.update(readed=True)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@user_passes_test(lambda u: u.is_superuser)
def ytb_playlist(request):
    navmenu = get_user_menu(request)
    playlist = YtbForms()

    if request.method == "POST":
        result, metadata = get_content(request.POST.get(
            'ytb_playlist_url'), request.POST.get('api_key'))
        ytb_playlist_url = request.POST.get('ytb_playlist_url')
        materi = PlaylistForms(initial={'ytb_playlist_url': request.POST.get('ytb_playlist_url'),
          'judul': metadata['title'],
          'pendek': metadata['description'], 
          'pengajar': metadata['channelTitle']})
        

        context = {'playlist': playlist, 'result': result, 'materi': materi, 'ytb_playlist_url': ytb_playlist_url, 'metadata': metadata}
        context = {**context, **navmenu}
        return render(request, 'edukasi/ytb_playlist.html', context)

    context = {'playlist': playlist}
    context = {**context, **navmenu}
    return render(request, 'edukasi/ytb_playlist.html', context)

@user_passes_test(lambda u: u.is_superuser)
def ytb_playlist_confirm(request):
    navmenu = get_user_menu(request)

    referer = request.META.get('HTTP_REFERER')
    if referer:
        if 'ytb_playlist/' not in referer:
            return redirect('ytb_playlist')
    else:
        return redirect('ytb_playlist')

    if request.method == "POST":
        judul = request.POST.get('judul')
        kode = request.POST.get('kode')
        pendek = request.POST.get('pendek')
        deskripsi = request.POST.get('deskripsi')
        pengajar = request.POST.get('pengajar')
        tentang_pengajar = '.'
        ytb_playlist_url = request.POST.get('ytb_playlist_url')

        try:
            pengajar = Pengajar.objects.get(nama=pengajar)
        except:
            pengajar = Pengajar.create_pengajar(nama=pengajar, tentang_pengajar=tentang_pengajar)
            pengajar.save()

        materi = Materi.objects.create(
            judul=judul,
            kode=kode,
            pendek=pendek,
            deskripsi=deskripsi,
            pengajar=pengajar,
            ytb_playlist_url=ytb_playlist_url,
            hidden=True,
            playlist=True,
        )

        result = request.POST.get('result')
        result = ast.literal_eval(result)
        mmt = Materi.objects.get(id=materi.pk)

        for k, i in enumerate(result):
            nn = Topic.objects.create(materi=mmt, no_urut=int(k), judul=str(
                i[0]), jenis='Link Video', link=str(i[1]), isi_tambahan=str(i[1]))

        return redirect('materi', materi.pk)

    context = {**context, **navmenu}
    return render(request, 'edukasi/ytb_playlist_confirm.html', context)

def view_kegiatan(request, sid):
    navmenu = get_user_menu(request)

    kegiatan = Kegiatan.objects.get(id=sid)
    materis = Materi.objects.filter(id=kegiatan.materi.id)

    context = {'kegiatan': kegiatan, 'materis': materis}
    context = {**context, **navmenu}
    return render(request, 'edukasi/kegiatan.html', context)


def list_kegiatan(request):
    navmenu = get_user_menu(request)

    kegiatan = Kegiatan.objects.all()
    context = {'kegiatan': kegiatan}
    context = {**context, **navmenu}
    return render(request, 'edukasi/listkegiatan.html', context)
    
def list_tugas_user(request, pk):
    navmenu = get_user_menu(request)

    pendaftaran = Pendaftaran.objects.filter(user=pk)
    jawaban = Jawaban.objects.filter(user=pk)
    lookup_user = User.objects.get(id=pk)

    all_jawaban = []
    for i in jawaban:
        all_jawaban.append(i.topic)
    

    data = {}
    for item in pendaftaran:
        tugas = Topic.objects.filter(materi_id = item.materi_id, tugas__isnull = False)
        data[item.materi.judul] = tugas

    import pprint
    pprint.pprint(jawaban)
    context = {'data': data, 'jawaban' : all_jawaban , 'lookup_user': lookup_user}
    context = {**context, **navmenu}
    return render(request, 'edukasi/list_tugas_user.html', context)

def cek_murid(request, pk):
    navmenu = get_user_menu(request)
    
    pendftr = Pendaftaran.objects.filter(materi_id=pk)

    import pprint
    pprint.pprint(pendftr )
    context = {'pendftr': pendftr}
    context = {**context, **navmenu}
    return render(request, 'edukasi/cek_murid.html', context)
