from distutils.command.upload import upload
from email.policy import default
from tkinter import CASCADE
from tokenize import Number
from xml.dom.minidom import CharacterData
from django.db import models
from django.dispatch import receiver
from django.forms import CharField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from PIL import Image


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)
    

# Create your models here.
class Manga(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    date = models.DateField()
    is_finished = models.BooleanField(default=False)
    image = models.ImageField(_('Image'), upload_to=upload_to, default='images/default.jpg')
    
    def save(self, *args, **kwargs):
        super().save()
        
        img = Image.open(self.image.path)
        width, height = img.size  # Get dimensions

        ratio = width/height
        
        if ratio < 3/4:
            new_height = 4*width/3
            top = (height - new_height)/2
            bottom = height - top
            left = 0
            right = width
            print(top, bottom)
            img = img.crop((left, top, right, bottom))
        elif ratio > 3/4:
            new_width = 3*height/4
            top = 0
            bottom = height
            left = (width - new_width)/2
            right = width - left
            print(left, right)
            img = img.crop((left, top, right, bottom))
        
        img.save(self.image.path)

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
    
    def add_friend(self, other_user):
        self.friends.add(other_user)
    
    
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