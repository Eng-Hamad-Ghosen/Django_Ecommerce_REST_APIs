from .models import Order, OrderItem
from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    orderItems= serializers.SerializerMethodField(method_name='get_order_items' , read_only=True)
    # orderItems= OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'city':{'required':True},
                        'zip_code':{'required':True},
                        'street':{'required':True},
                        'phone':{'required':True}}
        
    def get_order_items(self,obj):
        order_items= obj.orderitems.all()
        serializer=OrderItemSerializer(order_items,many=True)
        return serializer.data
    
    # from .models import OrderItem
    # def get_order_items(self,obj):
    #     order_items= OrderItem.objects.filter(order=obj)
    #     serializer=OrderItemSerializer(order_items,many=True)
    #     return serializer.data
    