from django.urls import path
from MyTvList import views 
app_name = 'MyTvList'
urlpatterns = [
    path('', views.index, name='index'),
    # index = Homepage.html
    path('createAccount/', views.createAccount, name='createAccount'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('topshows/', views.topshows, name='topshows'),
    path('recommended/', views.recommended, name='recommended'),
    path('castPage/', views.castPage, name='castPage'),
    path('showPage/', views.showPage, name='showPage'),
    path('watchListPage/', views.watchListPage, name='watchListPage'),
    path('showUser/', views.showUser, name='showUser'),
    path('addReview/', views.addReview, name='addReview'),
]
