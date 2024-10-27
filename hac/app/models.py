from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Book(models.Model):
     title = models.CharField(max_length=255, unique=True, blank=False, null=False)
     Book_Author = models.CharField(max_length=255, blank=False, null=False)
     Year_of_Publication = models.CharField(max_length=255, default='')
     Publisher = models.CharField(max_length=255,blank=False, null=False)
     img = models.CharField(max_length=255, null=False, default="")
     def __str__(self):
         return self.title  
     class Meta:
        db_table = 'book'  

class book_user(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     book = models.ForeignKey(Book, on_delete=models.CASCADE)
     user_rating = models.FloatField(blank=True)
     class Status(models.TextChoices):
         IN_PROCESS = 'IN_PROCESS'
         READ = 'READ'
     status = models.CharField(
         max_length=10,
         choices=Status.choices,
         default=Status.IN_PROCESS
     )
     def __str__(self):

        return f"{self.user_id}-{self.book_id}"
     class Meta:
         db_table = 'book_user'