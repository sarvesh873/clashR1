from django.urls import path
from . import views

urlpatterns = [
   
    path('quiz/',views.quiz, name='Quiz'),
    path('end/',views.endquiz, name='endquiz'),
    path('',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('register/',views.register,name='register'),
    path('start/',views.startQuiz,name='profile'),
    path('lifeline/',views.lifeline,name='lifeline'),
    path('red-zone/',views.red_zone,name='red_zone'),
    path('end-redzone/',views.endRZ,name='end-redzone'),
    path('save-timer/',views.saveTimer,name='save-timer'),
    path('result/',views.result,name='result'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path('leaderboard2/',views.leaderboard2,name='leaderboard2'),
    path('clashmugdha49/', views.emerglogin, name='emerglogin'),
    path('switchtab/', views.switchtab, name='switchtab'),
    path('skipped_red_zone/', views.skipped_red_zone, name='skipped_red_zone'),
    path('webteam/',views.webteam,name="webteam"),
    path('username/',views.usname,name="usname")
]

