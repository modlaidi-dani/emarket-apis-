from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import *  
from rest_framework.permissions  import IsAuthenticated , IsAdminUser 
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
# Create your views here.
@api_view(['POST'])
def regester(request):
    data =request.data
    user =SingupSerializer(data=data)
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user=User.objects.create(
                first_name=data['first_name'] ,
                last_name= data['last_name'],
                email= data['email'],
                username=data['email'],
                password=make_password(data['password']) 
            )
            return Response ({'detaill':'rejistrement reussit '}, status=status.HTTP_201_CREATED)
        else :
            return Response ({'erreur':'deja existé '}, status=status.HTTP_400_BAD_REQUEST)

    else :
        return Response (user.errors)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user=SingupSerializer(request.user,many=True)
    return Response (user.data)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updat_user(request):
    user=request.user
    data=request.data
    user.first_name=data['first_name'] 
    user.last_name= data['last_name']
    user.email= data['email']
    user.username=data['email']
    if data['password'] !="":
            user.password=make_password(data['password']) 
    user.save()
    serilaz=UserSerializer(user,many=False)
    return Response({"user":serilaz.data})
def get_current_host(request):
    protocol= request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol,host=host)
@api_view(['POST'])
def motdepasse_oublier(request):
    data=request.data
    user=get_object_or_404(User,email=data['email'])
    token= get_random_string(40)
    date_ex= datetime.now() + timedelta(minutes=5)
    user.profile.reset_password_token= token
    user.profile.reset_password_expire= date_ex
    user.profile.save()
    host=get_current_host(request)
    link='{host}api/reset_password/{token}'.format(host=host,token=token)
    body=" cliquez ici pour renitialiser ton mot de passe : {link}".format(link=link)
    send_mail(
        "Renitialisation de passeword de puis eMarket ",
        body ,
        "eMarket@gmail.com",
        [data['email']]        
    )
    return Response ({'details': 'un reset password est envoyé a l email: {email}'.format(email=data['email'])})
@api_view(['POST'])
def reset_password(request,token):
    data=request.data
    user=get_object_or_404(User,profile__reset_password_token=token)
    if user.profile.reset_password_expire.replace(tzinfo=None)< datetime.now():
        return Response ({'erreur':'remps experé'},status=status.HTTP_408_REQUEST_TIMEOUT)
    if data['password'] != data['confirmPassword']:
        return Response ({'erreur':'confirm passeword'},status=status.HTTP_400_BAD_REQUEST)
    user.password=make_password(data['password'])
    user.profile.reset_password_token= ""
    user.profile.reset_password_expire= None
    user.profile.save()
    user.save()
    return Response({'details':'Password done'})
    
            
    