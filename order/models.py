from django.db import models
from django.contrib.auth.models import User
from operator import mod
from django_countries.fields import CountryField
from product.models import Product
# Create your models here.

class OrderStatus(models.TextChoices):
    PROCESSING = 'PROCESSING'
    SHIPPED = 'SHIPPED'
    DELEVERD = 'DELEVERD'
    
class PaymentStatus(models.TextChoices):
    PAID = 'PAID'
    UNPAID = 'UNPAID'
    
class PaymentMode(models.TextChoices):
    CASH_ON_DELEVERD = 'CASH_ON_DELEVERD'
    CARD = 'CARD'
    

class Order(models.Model):
    city = CountryField(blank=True, null=True)
    zip_code = models.CharField(max_length=100 ,default='',blank=True)
    street = models.CharField(max_length=100 ,default='',blank=True)
    phone = models.CharField(max_length=100 ,default='',blank=True)
    total_amount = models.IntegerField(default=0)
    payment_status= models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_mode= models.CharField(max_length=30, choices=PaymentMode.choices,default=PaymentMode.CASH_ON_DELEVERD)
    order_status= models.CharField(max_length=30, choices=OrderStatus.choices,default=OrderStatus.PROCESSING)
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    product= models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    order= models.ForeignKey('Order' ,null=True,on_delete=models.CASCADE ,related_name='orderitems')
    name = models.CharField(max_length=200 , default='', blank=True)
    quntity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7,decimal_places=2, blank=True)

    
    def __str__(self):
        return str(self.name)

 