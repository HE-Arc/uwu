from django.contrib.auth.models import User
from rest_framework import serializers
from uwu.uwuapp.models import Chapter, FriendRequest, Manga, UwuUser

class UserSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['url', 'username', 'pk', 'image']
        
    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(UwuUser.objects.get(user=obj).image.url)
        
              

class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chapter
        fields = ['url', 'manga_id', 'order', 'title', 'page_nb', 'pk']
        
    

class MangaSerializer(serializers.HyperlinkedModelSerializer):
    chapters = serializers.HyperlinkedIdentityField(view_name='chapter-detail', many=True)
    isFinished = serializers.BooleanField(source='is_finished')
    
    class Meta:
        model = Manga
        fields = ['url', 'name', 'author', 'description', 'date', 'created', 'updated', 'isFinished', 'chapters', 'image', 'pk']
        
class UwuUserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    favorites = MangaSerializer(many=True, read_only=True)
    
    class Meta:
        model = UwuUser
        fields = ['url', 'username', 'friends', 'favorites', 'readed', 'image', 'pk']
        
class FriendRequestSerializer(serializers.HyperlinkedModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['url', 'sender', 'receiver', 'is_on_hold', 'timestamp', 'pk']