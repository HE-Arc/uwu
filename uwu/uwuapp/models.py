from tkinter import CASCADE
from tokenize import Number
from xml.dom.minidom import CharacterData
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User

# Create your models here.
class Manga(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    date = models.DateField()
    is_finished = models.BooleanField()
    chapter_nb = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Chapter(models.Model):
    manga_id = models.ForeignKey(Manga, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    page_nb = models.IntegerField()
    order = models.IntegerField()

    def __str__(self):
        return f'{self.order}: {self.title}'
    
class IsFriend(models.Model):
    user1_id = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2_id = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
    
class HasRead(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    