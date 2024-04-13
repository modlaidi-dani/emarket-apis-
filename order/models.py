from django.db import models
from operator import mod
from django.contrib.auth.models import User
from produit.models import Produit
# Create your models here.
class Orderstatus(models.TextChoices):
    PROCESSING ='Peocessing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
class PaymentStatus(models.TextChoices):
    PAID = 'Paid'
    UNPAID = 'Unpadid'
class PaymentMode(models.TextChoices):
    COD ='COD'
    CARD ='CARD'

class Order (models.Model):
    city = models.CharField( max_length=400,default='',blank=False)
    zip_code = models.CharField( max_length=100,default='',blank=False)
    street = models.CharField( max_length=400,default='',blank=False)
    state = models.CharField( max_length=100,default='',blank=False)
    country = models.CharField( max_length=100,default='',blank=False)
    phone_n = models.CharField( max_length=100,default='',blank=False)
    total_amount = models.IntegerField(default=0)
    payment_status = models.CharField( max_length=50,choices=PaymentStatus.choices,default=PaymentStatus.UNPAID)
    payment_mode = models.CharField( max_length=50,choices=PaymentMode.choices,default=PaymentMode.COD)
    status = models.CharField(max_length=60,choices=Orderstatus.choices,default=Orderstatus.PROCESSING)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    creatAt= models.DateTimeField( auto_now_add=True)
    def __str__(self):
        return str(self.id)

class OrderItem (models.Model):
    produit = models.ForeignKey(Produit, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE,related_name='orderitemes')
    name = models.CharField( max_length=200,default='',blank=False)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField( max_digits=7, decimal_places=2,blank=False)
    def __str__(self):
        return str(self.id)
