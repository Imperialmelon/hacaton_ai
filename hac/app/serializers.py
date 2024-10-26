from rest_framework import serializers
from .models import Book,User_Book,User
class BookSerializaer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields = ['pk', 'title', 'Book_Author', 'Year_of_Publication', 'Publisher', 'img']

class User_BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Book
        fields = ['book', 'user_rating']
        read_only_fields = ['book']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']