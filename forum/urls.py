from django.urls import path 
from . import views 

urlpatterns = [
    path('' , views.index , name = 'index'),
    path('login/' , views.login , name = 'login'),
    path('register/' ,views.register , name = 'register'),
    path('space/' , views.space , name = 'space'),
    path('logout/', views.logout_view , name = 'logout'),
    path('post/' , views.postThread , name = 'post'),
    path('resetpassword/',views.forgotView , name='forgot'),
    path('profile/<str:username>/',views.profile , name='profile')
]