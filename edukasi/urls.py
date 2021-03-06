from django.urls import path, include, re_path
from edukasi import views


from . import views
from . import apiviews
 

urlpatterns = [
    path('', views.homePage, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name="logout"),
    path('listmateri/', views.listmateri, name='listmateri'),
    path('materi/<str:sid>/', views.materi, name='materi'),
    path('topic/<str:sid>/', views.topic, name='topic'),
    path('kontribusi/', views.kontribusi, name='kontribusi'),
    path('faq/', views.faq, name='faq'),
    path('feature/', views.feature, name='feature'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('please_verify/', views.please_verify, name='please_verify'),
    path('messages/', views.messages, name='messages'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_materi/', views.add_materi, name='add_materi'),
    path('add_materi_topic/<str:sid>/', views.add_materi_topic, name='add_materi_topic'),
    path('edit_materi/<str:sid>/', views.edit_materi, name='edit_materi'),
    path('edittopic/<str:sid>/', views.edittopic, name='edittopic'),
    path('deltopic/<str:sid>/', views.deltopic, name='deltopic'),
    path('listtugas/', views.listtugas, name='listtugas'),
    path('add_tugas/', views.addtugas, name='addtugas'),
    path('edittugas/<str:sid>', views.edittugas, name='edittugas'),
    path('deletetugas/<str:sid>', views.deletetugas, name='deletetugas'),
    path('listsoal/', views.listsoal, name='listsoal'),
    path('add_soal/<str:sid>/', views.addsoal, name='addsoal'),
    path('editsoal/<str:sid>/', views.editsoal, name='editsoal'),
    path('deletesoal/<str:sid>/', views.deletesoal, name='deletesoal'),
    path('materisaya/', views.materisaya, name='materisaya'),
    path('listdiskusi/', views.listdiskusi, name='listdiskusi'),
    path('editdiskusi/<str:sid>/', views.editdiskusi, name='editdiskusi'),
    path('deletediskusi/<str:sid>/', views.deletediskusi, name='deletediskusi'),
    path('daftarmateri/<str:sid>/', views.daftarmateri, name='daftarmateri'),
    path('favorit/<str:sid>/', views.favorit, name='favorit'),
    path('listpembayaran', views.listpembayaran, name='listpembayaran'),
    path('setujupembayaran/<str:sid>/', views.setujupembayaran, name='setujupembayaran'),
    path('tolakpembayaran/<str:sid>/', views.tolakpembayaran, name='tolakpembayaran'),
    path('tugas/<str:sid>/', views.tugas, name='tugas'),
    path('periksa/<str:sid>/', views.periksa, name='periksa'),
    path('listjawaban/', views.listjawaban, name='listjawaban'),
    path('editjawaban/<str:sid>/', views.editjawaban, name='editjawaban'),
    path('readall/', views.readall, name='readall'),
    path('ytb_playlist/', views.ytb_playlist, name='ytb_playlist'),
    path('ytb_playlist_confirm/', views.ytb_playlist_confirm, name='ytb_playlist_confirm'),
    path('example_view/', apiviews.example_view, name='example_view'),
    path('api/topic/<int:pk>/', apiviews.topic_apiview, name='topic_apiview'),
    path('api/materi/<int:pk>/', apiviews.materi_apiview, name='materi_apiview'),
    path('api/listmateri/', apiviews.listmateri_apiview, name='listmateri_apiview'),
    path('api/message/', apiviews.message_apiview, name='message_apiview'),
    path('api/user/<int:pk>/', apiviews.user_apiview, name='user_apiview'),
    path('api/pendaftaran/', apiviews.pendaftaran_apiview, name='pendaftaran_apiview'),
    path('api/mendaftar/<int:pk>/', apiviews.mendaftar_apiview, name='mendaftar_apiview'),
    path('api/favorit/', apiviews.favorit_apiview, name='pendaftaran_apiview'),
    path('api/pembayaran/', apiviews.pembayaran_apiview, name='pembayaran_apiview'),
    path('api/tugas/<int:pk>/', apiviews.tugas_apiview, name='tugas_apiview'),
    path('api/soal/<int:pk>/', apiviews.soal_apiview, name='soal_apiview'),
    path('api/view_topic/<int:pk>/', apiviews.view_topic, name='view_topic'),
    path('kegiatan/<str:sid>/', views.view_kegiatan, name='view_kegiatan'),
    path('listkegiatan/', views.list_kegiatan, name='list_kegiatan'),
]
