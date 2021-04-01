from django.urls import path
from MyTvList import views 
app_name = 'MyTvList'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('topshows/', views.topshows, name='topshows'),
    path('recommended/', views.recommended, name='recommended'),
    path('addshow/', views.add_show, name='add_show'),
]