from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order, OrderItem
from product.models import Product
from .serializers import OrderSerializer, OrderItemSerializer





@api_view(['GET'],)
@permission_classes([IsAuthenticated])
def get_all_order(request):
    order = Order.objects.all()
    
    serializer = OrderSerializer(order,many=True)
    return Response(serializer.data)

@api_view(['GET'],)
@permission_classes([IsAuthenticated])
def get_order(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response({'error':'Your Order Not Found In Orders Model, Please Select Other Id'},status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['POST'],)
@permission_classes([IsAuthenticated])
def new_order(request):
    # order=Order.objects.all()
    if not 'orderItems' in request.data:
        return Response({'error':'No orderItems'},status=status.HTTP_400_BAD_REQUEST)
    else:
        orderItems=request.data['orderItems']
        print('1')
        # total_amount=sum(item['price']* item['quantity'] for item in orderItems)
        total_amount=0
        for item in orderItems:
            total_amount += int(item['price']) * int(item['quantity'])
            print('*2*\n')
        print('3')
        city = request.data['city']
        print('4')
        zip_code = request.data['zip_code']
        street = request.data['street']
        phone = request.data['phone']
        total_amount = total_amount
        obj_order=Order.objects.create(city=city, zip_code=zip_code, street=street, phone=phone, total_amount=total_amount, user=request.user)
        
        for i in orderItems:
            product = Product.objects.get(id=i['product'])
            obj_orderItem = OrderItem.objects.create(product=product,
                                                     order=obj_order,
                                                     name=product.name,
                                                     quantity=i['quantity'],
                                                     price=i['price'])
            product.stock -=obj_orderItem.quantity
            product.save()
        serializer= OrderSerializer(obj_order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
@api_view(['PUT'],)
@permission_classes([IsAuthenticated])
def update_order(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response({'error':'Your Order Not Found, Please Select Other Id'})
    from .models import OrderStatus
    o=OrderStatus.values
    if not 'order_status' in request.data:
        return Response({'order_status':'this is field is required'})
    
    if not request.data['order_status'] in o:
        print('\n Outtttt \n')
        return Response({'Error':{'please select from':{'1':'SHIPPED','2':'DELEVERD','3':'PROCESSING'}}},status=status.HTTP_400_BAD_REQUEST)
    order.order_status = request.data['order_status']
    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['DELETE'],)
@permission_classes([IsAuthenticated])
def delete_order(request,id):
    try:
        order = Order.objects.get(id=id)
        order.delete()
        return Response({'message':'Order delete dome'},status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error':'Your Order Not Found, Please Select Other Id'})