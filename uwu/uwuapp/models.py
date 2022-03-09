from distutils.command.upload import upload
from tkinter import CASCADE
from tokenize import Number
from xml.dom.minidom import CharacterData
from django.db import models
from django.dispatch import receiver
from django.forms import CharField
from django.contrib.auth.models import User


# Create your models here.
class Manga(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    date = models.DateField()
    is_finished = models.BooleanField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
    
class Chapter(models.Model):
    manga_id = models.ForeignKey(Manga, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    page_nb = models.IntegerField()
    order = models.IntegerField()

    def __str__(self):
        return f'{self.order}: {self.title}'

class UwuUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    favorites = models.ManyToManyField(Manga, blank=True, related_name='favorites') 
    readed = models.ManyToManyField(Chapter, blank=True, related_name='readed') 

    def __str__(self):
        return str(self.user)
    
    
    def remove_friend(self, other_user):
        """
        Remove a friend
        """
        try:
            self.friends.remove(other_user)
        except Exception as e:
            print(f"error! : {e}")
            
    def is_friend(self, other_user):
        """
        Is this user friend with the 'other_user'?
        """
        if other_user in self.friends:
            return True
        return False

class FriendRequest(models.Model):
    """
    A 'FriendRequest' has one sender and a receiver. 
    It can be on hold or not and a timestamp is created on the add action.
    """

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    is_on_hold = models.BooleanField(blank=True, null=False, default=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Accept a friend request
        Update both 'sender' and 'receiver' 'friends' field
        """
        self.receiver.uwuuser.add_friend(self.sender)
        self.sender.uwuuser.add_friend(self.receiver)
        self.is_on_hold = False
        self.save()

    def decline(self):
        """
        Decline a friend request by setting 'is_on_hold' field to False
        """
        self.is_on_hold = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request by setting 'is_on_hold' field to False
        """
        self.is_on_hold = False
        self.save()