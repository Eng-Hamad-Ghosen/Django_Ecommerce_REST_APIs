from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=7 ,decimal_places=2)
    brand =models.CharField(max_length=50)
    category = models.ForeignKey('Category',related_name='product_category',on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2,decimal_places=1 ,validators=[MinValueValidator(0.1),MaxValueValidator(5.0)])
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user =models.ForeignKey(User,on_delete=models.CASCADE)#or SET_NULL
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


