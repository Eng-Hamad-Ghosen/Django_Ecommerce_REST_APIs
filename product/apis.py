from rest_framework.decorators import api_view
from .models import Product
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer



@api_view(['GET','POST'])
def product_list(request):
    product=Product.objects.all()
    if request.method=='GET':
        serializer=ProductSerializer(product,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method=='POST':
        pass
    
@api_view(['GET','PUT','DELETE'])
def product_id(request, id):
    product=Product.objects.get(id=id)
    if request.method=='GET':
        pass
    if request.method=='PUT':
        pass
    if request.method=='DELETE':
        pass