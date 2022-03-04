from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from uwu.uwuapp.serializers import UserSerializer, MangaSerializer
from uwu.uwuapp.models import Manga

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
