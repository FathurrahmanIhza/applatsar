from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from applatsar.views import *


urlpatterns = [
    path('', index, name='index'),
    path('sejarah/', sejarah),
    path('visimisi/', visimisi),
    path('pegawai/', pegawai),
    path('gempadirasakan/', gempadirasakan),
    path('gempaterkini/', gempaterkini),
    path('login/', LoginView.as_view(), name='login'),
    path('sigempa/', sigempa, name='sigempa'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('sigempa/gambar/<int:id>', gambar, name='gambar'),
    path('sitamu/', sitamu, name='sitamu'),
    path('siritamu/', siritamu, name='siritamu'),
    path('sisensor/', sisensor, name='sisensor'),
    
]
