from django.urls import path
from. import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_Details/',views.user_Details,name='user_Details')
]