from django.contrib.auth.models import User
from rest_framework import serializers
from uwu.uwuapp.models import Manga

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']

class MangaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manga
        fields = ['url', 'name', 'author', 'date', 'is_finished']