from django.shortcuts import render, redirect
from .models import Book, book_user
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
import uuid
from .permissions import IsAuth
from .auth import Auth_by_Session
from .redis import session_storage
from datetime import datetime
from dateutil.parser import parse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token as T
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
import csv
import psycopg2
import pandas as pd

@api_view(['GET'])
@permission_classes([IsAuth])
@authentication_classes([Auth_by_Session])
def get_user_books(request):
    user_books = book_user.objects.filter(user = request.user)
    book_ids = [ub.book_id for ub in user_books]
    books = Book.objects.filter(pk__in=book_ids)
    serializer = BookSerializaer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def estimate_book(request, pk):
        book_id = 2
        book_for_user = book_user.objects.filter(user_id=pk, book_id=book_id).first()
        print(book_for_user) 
        serializer = User_BooksSerializer(book_for_user, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


     

import numpy as np
from django.db import connection

def get_dataframe_from_table():

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM book_user")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        return df
def func():

    data = get_dataframe_from_table()

    col_drop = data.columns[0]
    data.drop(columns = [col_drop], inplace = True)

    # Косинусное расстояние
    def cosine_similarity_manual(matrix):
        # Нормализируем
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        normalized_matrix = matrix / norms
        # Матричное произведение нормальной матрицы на транспонированную
        similarity_matrix = np.dot(normalized_matrix, normalized_matrix.T)
        return similarity_matrix

    def create_user_item_matrix_from_df(df):
        # Уникальные пользователи и книги
        users = df['user_id'].unique()
        print(type(users))
        tmp = []
        for u in users:
            tmp.append(u.item())

        books = df['book_id'].unique()
        user_index = {}
        for idx, u in enumerate(tmp):
            user_index[u] = idx
        
        tmp.clear()
        book_index = {}
        for b in books:
            tmp.append(b.item())
        for idx, b in enumerate(tmp):
            book_index[b] = idx
        # Массивы юзеров и книг
        # user_index = {user: idx for idx, user in enumerate(users)}
        # book_index = {book: idx for idx, book in enumerate(books)}
        print(user_index)

        # Матрица соотношений из нулей
        user_item_matrix = np.zeros((len(users), len(books)))

        # Делаем финальную матрицу
        for _, row in df.iterrows():
            user = row['user_id']
            book = row['book_id']
            rating = row['user_rating']
            user_item_matrix[user_index[user], book_index[book]] = rating

        return user_item_matrix, user_index, book_index



    def collaborative_filtering_recommendations(df, target_user_id, num_recommendations=5):

        user_item_matrix, user_index, book_index = create_user_item_matrix_from_df(df)


        # TODO:
        # Исправить момент, предлагать добавить книги
        # if target_user_id not in user_index:
        #     return f"User-ID {target_user_id} not found in the dataset."



        # Высчитываем матрицу похожести
        user_similarity = cosine_similarity_manual(user_item_matrix)

        # Находим похожих пользователей(исключаем самого юзера)
        target_user_idx = user_index[target_user_id]
        similar_users = np.argsort(-user_similarity[target_user_idx])[1:]

        # Считаем средневзвешенное по схожести
        similar_users_ratings = user_item_matrix[similar_users]
        avg_ratings = np.true_divide(similar_users_ratings.sum(axis=0), (similar_users_ratings != 0).sum(axis=0))

        # Исключаем уже оцененные книги
        user_rated_books = user_item_matrix[target_user_idx] > 0
        avg_ratings[user_rated_books] = 0

        # Выбираем лучшие N книг
        recommended_book_indices = np.argsort(-avg_ratings)[:num_recommendations]

        # Возврщаемся назад к ISBN
        index_to_book = {idx: book for book, idx in book_index.items()}
        recommended_books = [index_to_book[idx] for idx in recommended_book_indices]

        print('GOOOOOOL')
        return recommended_books

    # Пример
    target_user_id = 2
    recommended_books = collaborative_filtering_recommendations(data, target_user_id)
    print(recommended_books) 


@api_view(['GET'])
def calc(request):  
    func()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """
    Создание пользователя
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response('Creation failed', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username,password)
    user = User.objects.filter(username=username,password=password)
    print(user)
    if user is not None:
        session_id = str(uuid.uuid4())
        session_storage.set(session_id, username)
        response = Response(status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", session_id, samesite="lax")
        return response
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuth])
def logout_user(request):

    """
    деавторизация
    """
    session_id = request.COOKIES["session_id"]
    print(session_id)
    if session_storage.exists(session_id):
        session_storage.delete(session_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_403_FORBIDDEN)