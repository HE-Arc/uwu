from django.contrib.auth.models import User
from rest_framework import serializers
from uwu.uwuapp.models import Chapter, FriendRequest, Manga, UwuUser

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'pk']
        

class UwuUserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = UwuUser
        fields = ['url', 'username', 'friends', 'favorites', 'readed', 'image']
              

class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chapter
        fields = ['url', 'manga_id', 'order', 'title', 'page_nb', 'pk']

class MangaSerializer(serializers.HyperlinkedModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    isFinished = serializers.BooleanField(source='is_finished')
    
    class Meta:
        model = Manga
        fields = ['url', 'name', 'author', 'description', 'date', 'isFinished', 'chapters', 'image', 'pk']
        
        
class FriendRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'