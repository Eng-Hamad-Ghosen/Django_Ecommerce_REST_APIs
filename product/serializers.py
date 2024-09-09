from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
        # exclude =['user']
        extra_kwargs={
                    'user' : {
                                'write_only' : False ,
                                'required' : False
                             } 
                    }