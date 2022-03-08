from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.db.utils import IntegrityError
from rest_framework import viewsets, permissions, filters, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from uwu.uwuapp.serializers import ChapterSerializer, UserSerializer, MangaSerializer
from uwu.uwuapp.models import Chapter, Manga, UwuUser

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def add_friend(self, request, pk=None):
        """
        Add a new friend
        """
        user = User.objects.get(pk=pk)
        other_user = User.objects.get(username=request.data['other_user'])
        try:
            user.friends.create(user=other_user)
            other_user.friends.create(user=user)
            return Response(status.HTTP_200_OK, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(status.HTTP_409_CONFLICT, status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['post'])
    def unfriend(self, request, pk=None):
        """
        Unfriendinmg someone from the 'friends'
        """       
        user = User.objects.get(pk=pk)
        other_user = User.objects.get(username=request.data['other_user'])

        user_uwu = UwuUser.objects.get(user=user)
        other_user_uwu = UwuUser.objects.get(user=other_user)
        try:
            user_uwu.remove_friend(other_user)
            other_user_uwu.remove_friend(user)
            return Response(status.HTTP_200_OK, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(status.HTTP_409_CONFLICT, status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['post'])
    def is_friend(self, other_user):
        """
        Is this user friend with the 'other_user'?
        """
        if other_user in self.friends:
            return True
        return False

class MangaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mangas to be viewed or edited.
    """
    queryset = Manga.objects.all().order_by('-pk').reverse()
    serializer_class = MangaSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['is_finished']
    search_fields = ['name', 'author']
    ordering_fields = ['name', 'author', 'date']
    
class ChapterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chapters to be viewed or edited.
    """
    queryset = Chapter.objects.all().order_by('-order')
    serializer_class = ChapterSerializer
