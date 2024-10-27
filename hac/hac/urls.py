"""
URL configuration for hac project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
import pandas as pd

# def  fill_books():
#     from app.models import Book
#     from dateutil.parser import parse
#     data = pd.read_csv('/home/student/t/books_info_cut_2 (1).csv')
#     for index, row in data.iterrows():
#     # 1. Обработка данных книги
#         book_data = {
#         'title': row['title'],
#         'Book_Author': row['Book_Author'],
#         'Year_of_Publication': row['Year_of_Publication'],
#         'Publisher': row['Publisher'],
#         'img': row['img'],
#         }
#         book, created = Book.objects.get_or_create(
#         title=book_data['title'],
#         defaults=book_data
#     )
        
# def fill_book_user():
#     from app.models import book_user
#     import random
#     data = pd.read_csv('/home/student/t/user_rating (1).csv')
#     for index, row in data.iterrows():
#         # 1. Обработка данных книги
#             book_user_data = {
#             'book_id': random.randint(1,768),
#             'user_id': random.randint(1,11),
#             'user_rating' : row['user_rating'],
#             }
#             try:
#                 book_user.objects.update_or_create(
#             user_id=book_user_data['user_id'],
#             book_id=book_user_data['book_id'],
#             defaults=book_user_data
#             )
#             except Exception as e:
#                  print(e)
        





urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', views.get_user_books),
    path('<int:pk>/rate', views.estimate_book),
    path('login/', views.login),
    path('logout/', views.logout_user)
]
