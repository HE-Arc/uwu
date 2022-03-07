from django.contrib.auth.models import User
from rest_framework import serializers
from uwu.uwuapp.models import Chapter, Manga, UwuUser

class UserSerializer(serializers.HyperlinkedModelSerializer):
    friends = serializers.CharField(source='user.favorites')
    favorites = serializers.CharField(source='user.favorites')
    readed = serializers.CharField(source='user.favorites')


    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'friends', 'favorites', 'readed']

class MangaSerializer(serializers.HyperlinkedModelSerializer):
    chapters = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='chapter-detail')
    isFinished = serializers.BooleanField(source='is_finished')
    
    class Meta:
        model = Manga
        fields = ['url', 'name', 'author', 'date', 'isFinished', 'chapters', 'image']
        
class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chapter
        fields = ['url', 'manga_id', 'order', 'title', 'page_nb']