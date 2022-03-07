from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from uwu.uwuapp.serializers import ChapterSerializer, UserSerializer, MangaSerializer
from uwu.uwuapp.models import Chapter, Manga

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True)
    def add_friend(self, other_user):
        """
        Add a new friend
        """
        if not other_user in self.friends:
            self.friends.add(other_user)

class MangaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mangas to be viewed or edited.
    """
    queryset = Manga.objects.all().order_by('-pk').reverse()
    serializer_class = MangaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['is_finished']
    search_fields = ['name', 'author']
    ordering_fields = ['name', 'author', 'date']
    
class ChapterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mangas to be viewed or edited.
    """
    queryset = Chapter.objects.all().order_by('-order')
    serializer_class = ChapterSerializer
