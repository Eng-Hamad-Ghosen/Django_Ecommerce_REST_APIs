from rest_framework.decorators import api_view,permission_classes
from .models import Product
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
import django_filters
from .filters import ProductFilter

from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticated


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def product_list(request):
    product=Product.objects.all()
    
    if request.method=='GET':
        paginator = PageNumberPagination()
        paginator.page_size=2
        queryset = paginator.paginate_queryset(product,request)
        
        serializer = ProductSerializer(queryset , many=True)
        # serializer=ProductSerializer(product,many=True)
        return Response({'Count of all products ':product.count(),'Products':serializer.data},status=status.HTTP_200_OK)
    
    if request.method=='POST':
        serializer=ProductSerializer(data=request.data)
        print(request.user)
        name=request.data['name']
        if serializer.is_valid():
            if not Product.objects.filter(name=name).exists():
                
                serializer.save(user=request.user)# Product.objects.create(**request.data,user=request.user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response({'Error':'The Product Is Already Exists'},status=status.HTTP_201_CREATED)
        else:      
            return Response(serializer.errors,status=status.HTTP_201_CREATED)
    
@api_view(['GET','PUT','DELETE'])
def product_id(request, id):
    product=Product.objects.all()
    if request.method=='GET':
        obj_filter=ProductFilter(request.GET,queryset= product)
        product=obj_filter.qs
        
        paginator=Paginator(product,20)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        # serializer=ProductSerializer(product,many=True)
        serializer=ProductSerializer(page_obj,many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)
    if request.method=='PUT':
        product = Product.objects.get(id=id)
        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            if product.user==request.user:
                serializer.save(user=request.user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'Error':'Sorry! Can\'t Edit This Product'},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    if request.method=='DELETE':
        product = Product.objects.get(id=id)
        if product.user==request.user:
            product.delete()
            return Response({'message':'Delete Action Is Done'},status=status.HTTP_200_OK)
        else:
            return Response({'Error':'Sorry! You Can\'t Delete This Product'},status=status.HTTP_403_FORBIDDEN)
            
