from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from PIL import Image
from datetime import datetime


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

def resize(wanted_ratio, img):
    width, height = img.size  # Get dimensions

    ratio = width/height
    
    if ratio < wanted_ratio:
        new_height = width/wanted_ratio
        top = (height - new_height)/2
        bottom = height - top
        left = 0
        right = width
        img = img.crop((left, top, right, bottom))
    elif ratio > wanted_ratio:
        new_width = height * wanted_ratio
        top = 0
        bottom = height
        left = (width - new_width)/2
        right = width - left
        img = img.crop((left, top, right, bottom))
    
    return img
    
    

# Create your models here.
class Manga(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    description = models.TextField(default='Description coming soon')
    date = models.DateField()
    is_finished = models.BooleanField(default=False)
    image = models.ImageField(_('Image'), upload_to=upload_to, default='images/default.jpg')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save()
        
        wanted_ratio = 3/4
        img = Image.open(self.image.path)
        
        img = resize(wanted_ratio, img)
        
        img.save(self.image.path)
        

    def __str__(self):
        return self.name
    
class Chapter(models.Model):
    manga_id = models.ForeignKey(Manga, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    page_nb = models.IntegerField()
    order = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save()
        self.manga_id.save()
        
    def __str__(self):
        return f'{self.order}: {self.title}'



class UwuUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    
    image = models.ImageField(_('Image'), upload_to=upload_to, default='images/default_user.png')

    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    favorites = models.ManyToManyField(Manga, blank=True, related_name='favorites') 
    readed = models.ManyToManyField(Chapter, blank=True, related_name='readed', through='Readed') 

    def save(self, *args, **kwargs):
        super().save()
        
        img = Image.open(self.image.path)
        wanted_ratio = 1
        
        img = resize(wanted_ratio, img)
        
        img.save(self.image.path)

    def __str__(self):
        return str(self.user)
    
    def add_friend(self, other_user):
        self.friends.add(other_user)
    
    def remove_friend(self, other_user):
        """
        Remove a friend
        """
        try:
            print(other_user in self.friends.all())
            self.friends.remove(other_user)
            print("other_user: " + str(other_user))
            print(self.friends.all()[0])
            print(other_user in self.friends.all())
        except Exception as e:
            print(f"error! : {e}")
            
    def is_friend(self, other_user):
        """
        Is this user friend with the 'other_user'
        """
        return other_user in self.friends.all()
    
    def is_readed(self, chapter):
        return chapter in self.readed.all()
    
    def add_chapter(self, chapter):
        self.readed.add(chapter)
        
    def remove_chapter(self, chapter):
        self.readed.remove(chapter)
    
    def is_fav(self, manga):
        return manga in self.favorites.all()

class Readed(models.Model):
    user = models.ForeignKey(UwuUser, related_name='readed_user', on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name='chapter', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)

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
        self.delete()

    def cancel(self):
        """
        Cancel a friend request by setting 'is_on_hold' field to False
        """
        self.is_on_hold = False
        self.save()