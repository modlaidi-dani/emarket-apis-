from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Caregory(models.TextChoices):
    COMPUTER = 'Computer'   
    KIDS = 'Kids'
    HOME = 'Home' 
    FOOD = 'Food'

class Produit(models.Model):
    name=models.CharField(max_length=200,default="",blank=False)
    discription=models.TextField(max_length=1000,default="",blank=False)
    price=models.DecimalField(max_digits=7, decimal_places=2,default=0)
    bland=models.CharField(max_length=200,default="",blank=False)
    category = models.CharField( max_length=50,choices=Caregory.choices)
    ratings=models.DecimalField(max_digits=3, decimal_places=2,default=0)
    stock=models.IntegerField(default=0)
    creatAt= models.DateTimeField( auto_now_add=True)
    user= models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
class Review(models.Model):
    produit=models.ForeignKey(Produit, null=True, on_delete=models.CASCADE, related_name='reviews')
    user= models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating=models.IntegerField(default=0)
    comment=models.TextField(max_length=1000,default="",blank=False)
    creatAt= models.DateTimeField( auto_now_add=True)
    def __str__(self):
        return self.comment
    