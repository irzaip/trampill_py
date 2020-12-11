from django.urls import path, include, re_path
from edukasi import views


from . import views
 

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
    path('add_materi/', views.add_materi, name='add_materi'),
    path('add_materi_topic/<str:sid>/', views.add_materi_topic, name='add_materi_topic'),
    path('edit_materi/<str:sid>/', views.edit_materi, name='edit_materi'),
    path('edittopic/<str:sid>/', views.edittopic, name='edittopic'),
    path('deltopic/<str:sid>/', views.deltopic, name='deltopic'),
    path('listujian/', views.listujian, name='listujian'),
    path('add_ujian/', views.addujian, name='addujian'),
    path('editujian/<str:sid>', views.editujian, name='editujian'),
    path('deleteujian/<str:sid>', views.deleteujian, name='deleteujian'),
    path('listsoal/', views.listsoal, name='listsoal'),
    path('add_soal/', views.addsoal, name='addsoal'),
    path('editsoal/<str:sid>/', views.editsoal, name='editsoal'),
    path('deletesoal/<str:sid>/', views.deletesoal, name='deletesoal'),
    path('materisaya/', views.materisaya, name='materisaya'),
    path('listdiskusi/', views.listdiskusi, name='listdiskusi'),
    path('editdiskusi/<str:sid>/', views.editdiskusi, name='editdiskusi'),
    path('deletediskusi/<str:sid>/', views.deletediskusi, name='deletediskusi'),
]
