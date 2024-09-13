from django.shortcuts import render
from rest_framework.decorators import api_view ,permission_classes
from django.contrib.auth.models import User
from .serializers import SignupSerializer ,UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . models import Profile
# Create your views here.

@api_view(['POST',])
def register(request):#Signup
    serializer = SignupSerializer(data=request.data)
    if serializer :
        print('0')
        if serializer.is_valid():
            print('2')
            if not User.objects.filter(email=request.data['email']).exists():
                first_name = request.data['first_name']
                last_name = request.data['last_name']
                print(first_name)
                email = request.data['email']
                username = request.data['email']
                password = make_password(request.data['password1'])
                print(password)
                user = User.objects.create(
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            username=username,
                            password=password)
                return Response(serializer.data ,status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'The Email Is Already Exists'} ,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':serializer.errors} ,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error':'The Field Is Not Enouph'} ,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def user_Details(request):
    user=User.objects.get(username=request.user)
    serializer =UserSerializer(user)
    return Response({'data':serializer.data},status=status.HTTP_200_OK)

@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def user_Update(request):
    print(request.data['first_name'])
    print(request.user.last_name)
    user=User.objects.get(username=request.user)
    print(user.username)
    print(str(request.user))
    serializer =UserSerializer(user,request.data)
    if serializer.is_valid():
        if str(user.username)==str(request.user):
            if not 'password' in request.data:
                serializer.save()
                return Response({'Note':'Without Edit Your Password','data':serializer.data},status=status.HTTP_200_OK)
            else:
                serializer.save(password=make_password(request.data['password']))
                return Response({'Note':'With Edit Your Password','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'Error':'Sorry! Can\'t Edit This Profile'},status=status.HTTP_403_FORBIDDEN)
    return Response(serializer.errors)
            

from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from django.core.mail import send_mail

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}".format(protocol=protocol, host=host)


@api_view(['POST',])
def forgot_password(request):
    if not 'email' in request.data:
        return Response({'Error':{'email':'this field is required'}})
    try:
        
        user = User.objects.get(email = request.data['email'])
    except User.DoesNotExist:
        return Response({'Error':'Your Email Not Found In Users, Please Use Valid Email'})
    
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    
    user.user_profile.reset_password_token = token
    user.user_profile.reset_password_expire= expire_date
    user.user_profile.save()
    
    # host=get_current_host(request)
    # link = '{host}/accounts/reset_password/token'.format(host=host)
    link = 'http://127.0.0.1:8000/accounts/reset_password/{token}'.format(token=token)
    
    body = 'Your Password Reset Link is {link}'.format(link=link)
    
    send_mail(
        "Password Reset From Ecommerce_APIs",
        body,
        'Ecommerce_Hamad@gmail.com',
        [request.data['email']]
    )
    
    return Response({'message':'Password Reset Link Sent To {email}'.format(email=request.data['email'])})

@api_view(['POST'],)
def reset_password(request,token):
    if not 'password' in request.data:
        return Response({'password':'This field is required','confirmPassword':'This field is required'})
    # user = User.objects.get(user_profile__reset_password_token = token)
    # if user.user_profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
    #     return Response({'error':'Your Token Is Expired'},status=status.HTTP_400_BAD_REQUEST)
    
    
    # if request.data['password'] != request.data['confirmPassword']:
    #     return Response({'error':'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
    # user.password=make_password(request.data['password'])
    # user.user_profile.reset_password_token = ''
    # user.user_profile.reset_password_expire = None
    # user.user_profile.save()
    # user.save()
    # return Response({'Message':'Password reset DONE'},status=status.HTTP_200_OK)
    
    profile = Profile.objects.get(reset_password_token = token)
    user = User.objects.get(username=profile.user)
    
    if profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error':'Your Token Is Expired'},status=status.HTTP_400_BAD_REQUEST)
    
    
    if request.data['password'] != request.data['confirmPassword']:
        return Response({'error':'Password are not same'},status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(request.data['password'])
    profile.reset_password_token = ''
    profile.reset_password_expire = None
    profile.save()
    user.save()
    return Response({'Message':'Password reset DONE'},status=status.HTTP_200_OK)
    