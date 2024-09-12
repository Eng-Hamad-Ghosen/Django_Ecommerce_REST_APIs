from django.urls import path
from . import apis
urlpatterns = [
    path('',apis.product_list,name='product_list'),
    path('<int:id>/',apis.product_id,name='product_id'),
    path('<int:id>/create_review/',apis.create_review,name='create_review'),
    path('<int:id>/delete_review/',apis.delete_review,name='delete_review'),
]