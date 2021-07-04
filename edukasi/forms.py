from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ckeditor.fields import RichTextField



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'first_name','last_name','username', 'email', 'password1', 'password2']
        labels = { 'first_name' : "Nama depan", 
            'email': 'Alamat Surel',
            'last_name': 'Nama Belakang',
            'username': 'Username',
            'password2': 'Konfirmasi Password'}
        help_texts = {'first_name': "Isi dengan nama depan anda.", 'password1': ""}


class ExampleForm(forms.Form):
    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

class MateriForm(ModelForm):
    class Meta:
        model = Materi
        fields = '__all__'
        help_texts = {
            'judul': 'Tulis judul yang anda inginkan disini.'
        }

class TugasForm(ModelForm):
    class Meta:
        model = Tugas
        fields = '__all__'


class SoalForm(ModelForm):
    class Meta:
        model = Soal
        fields = '__all__'

class DiskusiForm(ModelForm):
    class Meta:
        model = Diskusi
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'topic': forms.HiddenInput(),
            'pesan': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['user','materi','ulasan','rating']
        widgets = {
            'user': forms.HiddenInput(),
            'materi': forms.HiddenInput(),
          'ulasan': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

class JawabanForm(ModelForm):
    class Meta:
        model = Jawaban
        fields = '__all__'

class YtbForms(forms.Form):
    api_key = forms.CharField(
        label = 'api_key',
        max_length = 300,
        required = True,
    )
    ytb_playlist_url = forms.CharField(
        label = 'Youtube Playlist',
        max_length = 300,
        required = True,
        help_text = 'Isi dengan url yang ada parameter <list>'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-ytbForm'
        self.helper.form_class = 'YTBForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))


class PlaylistForms(forms.Form):
    KATEGORI = (
        ('Teknologi', 'Teknologi'),
        ('Bisnis', 'Bisnis'),
        ('Pengembangan Diri', 'Pengembangan Diri'),
        ('Batch Khusus', 'Batch Khusus'),
        ('Koding Playlist', 'Koding Playlist'),
        ('Projects', 'Projects'),
    )
    RATING = (
        ('dasar','dasar'),
        ('menengah', 'menengah'),
        ('mahir','mahir'),
    )

    judul = forms.CharField(max_length=200)
        
    kode = forms.CharField(max_length=20,)
    pendek = forms.CharField(max_length=300,)
    deskripsi = RichTextField()
    pengajar = forms.CharField(max_length=40)
    tentang_pengajar = RichTextField()
    hidden = forms.BooleanField()
    playlist = forms.BooleanField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-PlyForm'
        self.helper.form_class = 'PLYForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))
