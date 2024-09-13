from django.urls import path
from. import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_Details/',views.user_Details,name='user_Details'),
    path('user_Update/',views.user_Update,name='user_Update'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password/<str:token>',views.reset_password,name='reset_password'),
]