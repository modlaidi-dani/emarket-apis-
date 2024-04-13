from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .filters import *
from .serializers import ProduuitSerialiser
from .models import *
from django.db.models import Avg
# Create your views here.
@api_view(['GET'])
def all_poduit(request):
    #produits=Produit.objects.all()
    #serializer=ProduuitSerialiser(produits,many=True)

    filterset=monFilter(request.GET,queryset=Produit.objects.all().order_by('id'))
    page=PageNumberPagination()
    page.page_size=2
    querys=page.paginate_queryset(filterset.qs,request)
    serializer=ProduuitSerialiser(querys,many=True)
    
    return Response ({'produits': serializer.data})
@api_view(['GET'])
def poduit(request,pk):
    produit=get_object_or_404(Produit,id=pk)
    serializer=ProduuitSerialiser(produit,many=False)
    print (produit)
    return Response ({'produit': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creat_produit(request):
    data =request.data 
    serializer=ProduuitSerialiser(data=data)
    if serializer.is_valid():
        prodect=Produit.objects.create(**data,user=request.user)
        res=ProduuitSerialiser(prodect,many=False)
        return Response({'produit':res.data})
    else:
        return Response(serializer.errors)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def udate_produit(request,pk):
    produit=get_object_or_404(Produit,id=pk)
    if produit.user != request.user :
        return Response ({"erreur": " tu peut pas modifier se produit"}, status= status.HTTP_403_FORBIDDEN )
    produit.name=request.data["name"]
    produit.discription=request.data["discription"]
    produit.price=request.data["price"]
    produit.bland=request.data["bland"]
    produit.category=request.data["category"]
    produit.ratings=request.data["ratings"]
    produit.stock=request.data["stock"]
    
    produit.save()
    serilaz=ProduuitSerialiser(produit,many=False)
    return Response({"produit": serilaz.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def dlete(request,pk):
    produit=get_object_or_404(Produit,id=pk)
    if produit.user != request.user :
        return Response ({"erreur": " tu peut pas suprimer se produit"}, status= status.HTTP_403_FORBIDDEN )
    produit.delete()
    return Response({"succes":"le produit est suprimé"})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review(request,pk):
    user=request.user
    produit=get_object_or_404(Produit,id=pk)
    data=request.data
    review=produit.reviews.filter(user=user)
    if data['rating']<=0 or data['rating'] > 5:
        return Response ({"erreur": " chouses entre 0 et 5"}, status= status.HTTP_400_BAD_REQUEST )
    elif review.exists():
        new_review={'rating':data['rating'],'comment':data['comment']}
        review.update(**new_review)
        rating = produit.reviews.aggregate(avg_ratings=Avg('rating'))
        produit.ratings=rating['avg_ratings']
        produit.save()
        return Response ({"detail": "votre review est updaté"})
    else:
        Review.objects.create(
            user=user,
            produit=produit,
            rating=data['rating'],
            comment = data['comment'],
        )
    
        rating = produit.reviews.aggregate(avg_ratings=Avg('rating'))
        produit.ratings=rating['avg_ratings']
        produit.save()
        return Response ({"detail": "votre review est cree"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def review_dlete(request,pk):
    user = request.user
    produit= get_object_or_404(Produit,id=pk)
    review= produit.reviews.filter(user=user)
    if review.exists():
        review.delete()
        rating=produit.reviews.aggregate(avg_rating=Avg('rating'))
        if rating['avg_rating']is None:
            rating['avg_rating']=0
            produit.ratings=rating['avg_rating']
            produit.save()
            return Response ({'detels':'votre reviws est suprimé'})
        else:
            produit.ratings=rating['avg_rating']
            produit.save()
            return Response ({'detels':'votre reviws est suprimé'})
            
    else:
        return Response ({'erreur':'review pas trouvé'},status=status.HTTP_404_NOT_FOUND)
