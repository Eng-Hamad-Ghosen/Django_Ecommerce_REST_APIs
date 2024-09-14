from django.urls import path
from . import views
urlpatterns = [
    path('',views.get_all_order,name='get_all_order'),
    path('<int:id>/',views.get_order,name='get_order'),
    path('<int:id>/update/',views.update_order,name='update_order'),
    path('<int:id>/delete/',views.delete_order,name='delete_order'),
    path('new/',views.new_order,name='new_order'),
]