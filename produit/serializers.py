from rest_framework import serializers
from .models import *

class ProduuitSerialiser(serializers.ModelSerializer):
    review=serializers.SerializerMethodField(method_name='get_reviews',read_only=True)
    class Meta:
        model= Produit
        fields = ('__all__')
        #fields = ('name','price','bland') 
    def get_reviews(self,obj):
        reviws=obj.reviews.all()
        serializers=ReviewSerialiser(reviws,many=True)
        return serializers.data

class ReviewSerialiser(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields = ('__all__')
