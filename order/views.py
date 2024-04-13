from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user=request.user
    data= request.data
    order_itemes=data['order_itemes']
    if order_itemes and len(order_itemes)==0:
        return Response({'erreur':'no order recived'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order=Order.objects.create(
            user=user,
            city=data['city'],
            zip_code=data['zip_code'],
            street=data['street'],
            phone_n=data['phone_n'],
            country=data['country'],
        )
        total_amount=0
        for i in order_itemes:
            produit = Produit.objects.get(id=i['produit'])
            if i['quantity'] <= produit.stock:    
                price=produit.price
                item=OrderItem.objects.create(
                    produit=produit,
                    order=order,
                    name=produit.name,
                    quantity=i['quantity'],
                    price=price
                )
                total_amount+=(i['quantity']* price )
                produit.stock -=item.quantity
                produit.save()
            else: 
                return Response ({'erreur':'La quantité de produit {produit} est inufisante pour efictuer'.format(produit=produit.name)},status=status.HTTP_406_NOT_ACCEPTABLE)
        order.total_amount=total_amount
        order.save()
        serializers=OrderSerializer(order,many=False)
        return Response(serializers.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orders(request):
    orders=Order.objects.all()
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)
