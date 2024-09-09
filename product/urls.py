from django.urls import path
from . import apis
urlpatterns = [
    path('',apis.product_list,name='product_list'),
    path('<int:id>/',apis.product_id,name='product_id'),
]