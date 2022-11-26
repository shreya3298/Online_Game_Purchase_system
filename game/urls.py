from django.urls import path,include
from . import views
urlpatterns = [
    path('index/',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('games/',views.games,name="games"),
    path('news/',views.news,name="news"),
    path('single/',views.single,name="single"),
    path('register/',views.register,name="register"),
    path('',views.login,name="login"),
    path('forgetpass/',views.forgetpass,name="forgetpass"),
    path('otp/' , views.otp, name="otp"),
    path('logout/',views.logout, name="logout"),
    path('addgame/',views.addgame, name="addgame"),
    path('viewgame/',views.viewgame, name="viewgame"),
    path('mygame/',views.mygame, name="mygame"),
    path('onlinegame/',views.onlinegame, name="onlinegame"),
    path('myprofile/',views.myprofile, name="myprofile"),
    path('donate/<int:pk>', views.donate, name="donate"),
    path('donate/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    

]