from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from uwu.uwuapp.serializers import ChapterSerializer, HasReadSerializer, IsFriendSerializer, UserSerializer, MangaSerializer
from uwu.uwuapp.models import Chapter, HasRead, IsFriend, Manga

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class MangaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mangas to be viewed or edited.
    """
    queryset = Manga.objects.all().order_by('-date')
    serializer_class = MangaSerializer
    
class ChapterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mangas to be viewed or edited.
    """
    queryset = Chapter.objects.all().order_by('-order')
    serializer_class = ChapterSerializer
    
class IsFriendViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mangas to be viewed or edited.
    """
    queryset = IsFriend.objects.all()
    serializer_class = IsFriendSerializer
    
class HasReadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mangas to be viewed or edited.
    """
    queryset = HasRead.objects.all()
    serializer_class = HasReadSerializer
