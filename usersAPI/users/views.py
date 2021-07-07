from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import query
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import status
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users import serializers

def login(request):
    user_name = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=user_name, password=password)
    if user is not None:
        return Response(user)
    else:
        return Response("Wrong credentials")
    
class Users(APIView):  
    
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request): 
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            from django.contrib.auth.hashers import make_password
            serializer.validated_data["password"] = make_password(request.data.get('password'))
            serializer.save()
        return Response("User saved")
    
    def put(self, request, id, format=None):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user,data=request.data)
        if serializer.is_valid(raise_exception=True):
            from django.contrib.auth.hashers import make_password
            serializer.validated_data["password"] = make_password(request.data.get('password'))
            serializer.save()
        return Response("User updated")
    
    def delete(self, request, id, format=None):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response("Successfully Deleted")
        except  User.DoesNotExist:
            return Response("User does not exist")
            
    
    
