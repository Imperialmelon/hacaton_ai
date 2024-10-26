from django.shortcuts import render, redirect
from .models import Book, User_Book
from django.core.exceptions import BadRequest
from django.db.models import Q, F
from django.db import connection
import psycopg2
from .serializers import BookSerializaer,User_BooksSerializer,UserSerializer
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import *
from django.core.files.uploadedfile import InMemoryUploadedFile
import os.path
from datetime import datetime
from dateutil.parser import parse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token as T
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

@api_view(['GET'])
def get_user_books(request , pk):
    user_books = User_Book.objects.filter(user_id = pk)
    book_ids = [ub.book_id for ub in user_books]
    books = Book.objects.filter(pk__in=book_ids)
    serializer = BookSerializaer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def estimate_book(request, pk):
        book_id = 2
        book_for_user = User_Book.objects.filter(user_id=pk, book_id=book_id).first()
        print(book_for_user)
        serializer = User_BooksSerializer(book_for_user, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fill_bd(request):
    try:
        for i in range(280001):
            user = {
                'username' : f'user{i}',
                'password' : 'djangopassword'
            }
            serializer = UserSerializer(data=user)
            if  serializer.is_valid():
                serializer.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
         return Response(e)
        