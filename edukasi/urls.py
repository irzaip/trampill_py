from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.homePage, name="home"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name="logout"),
    path('listmateri/', views.listmateri, name='listmateri'),
    path('materi/<str:sid>/', views.materi, name='materi'),
    path('edittopic', views.edittopic, name='edittopic'),    
    path('topic/<str:sid>/', views.topic, name='topic'),
]
