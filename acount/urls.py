from django.urls import path
from . import views

urlpatterns = [
    path('regester', views.regester, name='regester'),
    path('info', views.current_user, name='info'),
    path('update_user', views.updat_user, name='update_user'),
    path('forget_password', views.motdepasse_oublier, name='forgect_password'),
    path('reset_password/<str:token>', views.reset_password, name='rest_password'),
    
]