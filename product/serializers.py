from rest_framework import serializers
from .models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    avg_rating=serializers.IntegerField()
    class Meta:
        model=Product
        fields='__all__'
        # exclude =['user']
        extra_kwargs={'user' : {'write_only' : False , 'required' : False} }

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['rating','comment']