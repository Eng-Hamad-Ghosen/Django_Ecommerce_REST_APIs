from django.contrib.auth.models import User
from rest_framework import serializers


class SignupSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password1','password2']
        extra_kwargs={'first_name':{'required':True},
                      'last_name':{'required':True},
                      'email':{'required':True},
                      'password1':{'required':True},
                      'password2':{'required':True}
                      }

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The tow passwords do not match.")
        
        if len(data['password1']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        
        return data
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password']
        extra_kwargs={'password':{'write_only':True,'required':False}}