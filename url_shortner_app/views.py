from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import *
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .serializers import ShortURLSerializer
import qrcode
import io
import base64

@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_api(request):
    token=get_token(request)
    return JsonResponse({'csrfToken':token})

@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    user=User.objects.create_user(username=request.data['username'],password=request.data['password'])
    login(request,user)
    return Response({'username':user.username})

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    user=authenticate(username=request.data['username'],password=request.data['password'])
    if user:
        login(request,user)
        return Response({'username':user.username})
    return Response({'error':"invalid"},status=400)

@api_view(['POST'])
def logout_api(request):
    logout(request)
    return Response({'message':'Logged out successfully'})

@api_view(['GET'])
@permission_classes([AllowAny])
def check_auth_api(request):
    if request.user.is_authenticated:
        return Response({'isAuth':True,'username':request.user.username})
    return Response({'isAuth':False})

@api_view(['POST'])
@permission_classes([AllowAny])
def create_short_url(request):
    serializer=ShortURLSerializer(data=request.data)
    if serializer.is_valid():
        user=request.user if not isinstance(request.user,AnonymousUser) else None
        instance=serializer.save(user=user)
        full_url=f"http://127.0.0.1:8000/api/{instance.short_code}"
        qr_image=qrcode.make(full_url)
        buffer=io.BytesIO()
        qr_image.save(buffer,format='PNG')
        qr_base64 =base64.b64encode(buffer.getvalue()).decode()
        return Response({
            'id':instance.id,
            'original_url':instance.original_url,
            'short_url':full_url,
            'short_code':instance.short_code,
            'clicks':instance.clicks,
            'qr_code':f'data:image/png;base64,{qr_base64}'
        },status=201)
    return Response(serializer.errors,status=400)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_urls_api(request):
    urls=ShortURL.objects.filter(user=request.user)
    serializer=ShortURLSerializer(urls,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def redirect_original_page(request,short_code):
    url_obj=get_object_or_404(ShortURL,short_code=short_code)
    url_obj.clicks +=1
    url_obj.save(update_fields=['clicks'])
    return HttpResponseRedirect(url_obj.original_url)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_original_url_api(request,short_code):
    try:
        url=ShortURL.objects.get(short_code=short_code)
        url.clicks+=1
        url.save(update_fields=['clicks'])
        return Response({'original_url':url.original_url})
    except ShortURL.DoesNotExist:
        return Response({'error':'URL not found'},status=404)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def change_password(request):
#     user=request.user
#     old_password=request.data.get('old_password')
#     new_password=request.data.get('new_password')

#     if not user.check_password(old_password):
#         return Response({'error':'old password is wrong'},status=400)
#     try:
#         validate_password(new_password,user)
#     except ValidationError as e:
#         return Response({'error':'e.messages'},status=400)
    
#     user.set_password(new_password)
#     user.save()
#     return Response({'success':'password changed..'},status=200)


#--------------------------------------------------------------------------------

  