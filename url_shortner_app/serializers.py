from rest_framework import serializers
from .models import *

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShortURL
        fields=['id','original_url','short_code','created_at','clicks']
    

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','first_name','last_name','email']