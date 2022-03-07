from django.contrib.auth.models import User
from rest_framework import serializers
from uwu.uwuapp.models import Chapter, HasRead, IsFriend, Manga

class UserSerializer(serializers.HyperlinkedModelSerializer):
    user1 = serializers.StringRelatedField(many=True)
    user2 = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'user1', 'user2']

class MangaSerializer(serializers.HyperlinkedModelSerializer):
    chapters = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Manga
        fields = ['url', 'name', 'author', 'date', 'is_finished', 'chapter_nb', 'chapters']
        
class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chapter
        fields = ['url', 'manga_id', 'order', 'title', 'page_nb']

class IsFriendSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = IsFriend
        fields = ['url', 'user1_id', 'user2_id']
        
class HasReadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HasRead
        fields = ['url', 'user_id', 'chapter_id']