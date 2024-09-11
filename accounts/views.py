from django.shortcuts import render
from rest_framework.decorators import api_view ,permission_classes
from django.contrib.auth.models import User
from .serializers import SignupSerializer ,UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
            