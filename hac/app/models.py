from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Book(models.Model):
     title = models.CharField(max_length=255, unique=True, blank=False, null=False)
     author = models.CharField(max_length=255, blank=False, null=False)
     desc = models.TextField(blank=True)
     genre = models.CharField(max_length=255, blank=True)
     img = models.CharField(max_length=255, null=False, default="")
     isbn = models.IntegerField(null=False, blank=False)
     isbn13 = models.IntegerField(null=False, blank=False)
     link = models.CharField(max_length=255, null=False, default="")
     pages = models.IntegerField(validators=[MinValueValidator(1)])
     rating = models.FloatField()
     def str(self):
        return self.title   
     class Meta:
        db_table = 'book'  

class User_Book(models.Model):
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
     def str(self):
        return f"{self.user_id}-{self.book_id}"
     class Meta:
         db_table = 'User_Book'