import django
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.dispatch import receiver
from django_filters.rest_framework import DjangoFilterBackend
from requests import request
from rest_framework import viewsets, filters, status, pagination
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, IsAuthenticated 
from rest_framework.decorators import action
from rest_framework.response import Response
from uwu.uwuapp.serializers import ChapterSerializer, FriendRequestSerializer, UwuUserSerializer, MangaSerializer, UserSerializer
from uwu.uwuapp.models import Chapter, FriendRequest, Manga, UwuUser
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .permissions import *


title_param = openapi.Parameter('Title', openapi.IN_QUERY, description="chapter's title", type=openapi.TYPE_STRING, required=True)
page_nb = openapi.Parameter('Page nb', openapi.IN_QUERY, description="chapter's page number", type=openapi.TYPE_NUMBER, required=True)
order_nb = openapi.Parameter('Order', openapi.IN_QUERY, description="chapter's order", type=openapi.TYPE_NUMBER)

class UwuUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UwuUser.objects.all().order_by('pk')
    serializer_class = UwuUserSerializer       
    permission_classes = [IsAdminUser,]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['username',]
    permission_classes = [UserPermission,]
    
    def list(self, request):
        super_list = super().list(request)
        current_user = request.user
        
        for user in super_list.data['results']:
            if user['pk'] == current_user.pk:
                super_list.data['results'].remove(user)           
            
        return super_list

    
    def create(self, validated_data):
        try:
            user = User.objects.create(username=validated_data.data['username'])
            user.set_password(validated_data.data['password'])
            user.save()
            
            if 'image' in validated_data.data:
                user_uwu = UwuUser.objects.create(user=user, image=validated_data.data['image'])
            else:
                user_uwu = UwuUser.objects.create(user=user)

            user_uwu.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                                'status' : f'The user {user} has been created',
                                'token': token.key,
                            },
                            status=status.HTTP_202_ACCEPTED)
        except IntegrityError:
            return Response({
                                'status' : f'The username {validated_data.data["username"]} is already used',
                            },
                            status=status.HTTP_409_CONFLICT)
        except:
            user.delete()
    
    
    @action(detail=True, methods=['post'])
    def unfriend(self, request, pk=None):
        """
        Unfriending someone from the friends
        """       
        user = request.user
        other_user = User.objects.get(pk=pk)

        user_uwu = UwuUser.objects.get(user=user)
        other_uwu_user = UwuUser.objects.get(user=other_user)
        
        if user_uwu.is_friend(other_user):
            user_uwu.remove_friend(other_user)
            other_uwu_user.remove_friend(user)
            return Response({
                                'status' : f'{user} and {other_user} are not friend anymore',
                            }, 
                            status=status.HTTP_200_OK)
        else:
            return Response({
                                'status' : f'{user_uwu} and {other_uwu_user} are already not friend',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=True, methods=['post'])
    def cancel_friend(self, request, pk=None):
        """
        Cancel a friend request that has been send to the user {pk}
        """
        user = request.user
        other_user = User.objects.get(pk=pk)
        
        friend_request = FriendRequest.objects.get(sender=user, receiver=other_user, is_on_hold=True)
        
        if friend_request:
            friend_request.is_on_hold = False
            friend_request.save()
            return Response({'status':'Friend request has been cancel'}, status=status.HTTP_200_OK)
        return Response({'status':'A problem has been encounter'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def ask_friend(self, request, pk=None):
        """
        Try to add a friend request to the user {pk}
        """        
        user = request.user
        try:
            other_user = User.objects.get(pk=pk)
        except django.contrib.auth.models.User.DoesNotExist:
            return Response({
                                'status' : f'The user doesn\'t exist',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        
        if UwuUser.objects.get(user=user).is_friend(other_user):
            return Response({
                                'status' : f'{user} and {other_user} are already friend',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        if user == other_user:
            return Response({
                                'status' : 'You can\'t send a friend request to yourself',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        same_request = FriendRequest.objects.all().filter(sender = user, receiver = other_user, is_on_hold=True)
        reverse_request = FriendRequest.objects.all().filter(sender = other_user, receiver = user, is_on_hold=True)
        
        if same_request.count() > 0:
            return Response({
                                'status' : 'the same request already exist',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        if reverse_request.count() > 0:
            return Response({
                                'status' : f'{other_user} has already send a request to {user}',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        FriendRequest.objects.create(sender=user, receiver=other_user)
        return Response({
                            'status' : 'Friend request has been send',
                        },
                        status=status.HTTP_201_CREATED)
        
        
    @action(detail=True)        
    def get_friends(self, request, pk=None):
        """
        Get all friends
        """
        paginator = pagination.PageNumberPagination()
        context = {'request':request}
        user = User.objects.get(pk=pk)
        uwu_user = UwuUser.objects.get(user=user)
        results = uwu_user.friends.all().order_by('username')
        results = paginator.paginate_queryset(results, request)

        serializer = UserSerializer(results, many=True, context=context)
        
        response = paginator.get_paginated_response(serializer.data)

        return response

    @action(detail=True)        
    def get_readed(self, request, pk=None):
        """
        Get every chapters readed.
        """
        paginator = pagination.PageNumberPagination()
        context = {'request':request}
        user = User.objects.get(pk=pk)
        uwu_user = UwuUser.objects.get(user=user)

        results = uwu_user.readed.all()
        results = paginator.paginate_queryset(results, request)
        serializer = ChapterSerializer(results, many=True, context=context)
        response = paginator.get_paginated_response(serializer.data)

        return response

    @action(detail=True)        
    def get_favorites(self, request, pk=None):
        """
        Get favorties mangas.
        """
        paginator = pagination.PageNumberPagination()
        context = {'request':request}
        user = User.objects.get(pk=pk)
        uwu_user = UwuUser.objects.get(user=user)
        results = uwu_user.favorites.all().order_by('-date')

        serializer = MangaSerializer(results, many=True, context=context)
        results = paginator.paginate_queryset(results, request)        
        response = paginator.get_paginated_response(serializer.data)
        
        return Response(response.data, status=status.HTTP_200_OK)
    
    @action(detail=True)        
    def get_readed_mangas(self, request, pk=None):
        """
        Get every readed mangas.
        """
        paginator = pagination.PageNumberPagination()
        context = {'request':request}
        user = User.objects.get(pk=pk)
        uwu_user = UwuUser.objects.get(user=user)
        results = uwu_user.readed.all().order_by('page_nb')           

        if len(results) > 0:
            mangas = []
            for c in results:
                mangas.append(c.manga_id.pk)

            mangas = set(mangas)
            results = Manga.objects.filter(pk__in=mangas).all().order_by('pk')
                
            results = paginator.paginate_queryset(results, request)
            serializer = MangaSerializer(results, many=True, context=context)
            response = paginator.get_paginated_response(serializer.data)
            
            for r in response.data['results']:
                progress = 0
                if len(r['chapters']):
                    chapters = uwu_user.readed.all()
                    for c in r['chapters']:
                        if c.obj in chapters:
                            progress += 1
                    progress = progress*100/len(r['chapters'])
                
                r['progress'] = progress

            return response
        
        return Response({})

    @action(detail=True)
    def total_pages_readed(self, request, pk=None):
        """
        Get number of readed pages.
        """
        user = User.objects.get(pk=pk)
        user_uwu = UwuUser.objects.get(user=user)

        readed = user_uwu.readed.all()

        total = 0
        for c in readed:
            total += c.page_nb
        
        return Response({'pages_readed':total})

    @action(detail=False)
    def my_user(self, request):
        """
        Get the current user.
        """
        context = {'request':request}
        
        user = request.user
        
        serializer = UserSerializer(user, context=context)
        
        return Response(serializer.data)
    
    @action(detail=False)
    def is_admin(self, request):
        """
        Get True if the current user is an admin.
        """
        return Response({'is_admin':request.user.is_staff})
    
    @action(detail=True)
    def is_friend(self, request, pk=None):
        """
        Get True if the current user is friend with the user {pk}.
        """
        user = request.user
        uwu_user = UwuUser.objects.get(user=user)
        
        other_user = User.objects.get(pk=pk)
        other_uwu_user = UwuUser.objects.get(user=other_user)
        
        same_request = FriendRequest.objects.filter(sender = user, receiver = other_user, is_on_hold=True).all()
        other_request = FriendRequest.objects.filter(sender = other_user, receiver = user, is_on_hold=True).all()
        
        response = Response({})

        response.data['is_friend'] = other_user in uwu_user.friends.all()
        response.data['is_asked'] = bool(same_request or other_request)
        
        
        return response
        
    
    
class MangaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mangas to be viewed or edited.
    """
    queryset = Manga.objects.all().order_by('-updated')
    serializer_class = MangaSerializer
    permission_classes = [MangaPermission,]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['is_finished']
    search_fields = ['name', 'author']
    ordering_fields = ['name', 'author', 'date']
    
    @swagger_auto_schema(manual_parameters=[title_param, page_nb, order_nb], request_body=None, responses={200:openapi.Response('response description', ChapterSerializer)})
    @action(detail=True, methods=['post'])
    def add_chapter(self, request, pk=None):
        """
        It adds a chapter to a manga.
        """
        if not request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        context = {'request':request}
        manga = Manga.objects.get(pk=pk)
        
        serializer = MangaSerializer(manga, context=context)
        
        try:
            order = request.data['order']
        except:
            order = len(serializer.data['chapters']) + 1
        
        
        chapter = Chapter.objects.create(
            manga_id = manga,
            title = request.data['title'],
            page_nb = request.data['page_nb'],
            order = order
        )
        
        serializer = ChapterSerializer(chapter, context=context)
        if serializer.is_valid:
            chapter.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True)
    def get_chapters(self, request, pk=None):
        """
        Get all chapter from the manga.
        """
        context = {'request':request}
        queryset = Chapter.objects.all().filter(manga_id=pk).order_by('order')
        serializer = ChapterSerializer(queryset, many=True, context=context)
        
        if len(serializer.data) > 0:
            user = self.request.user
            if not isinstance(user, AnonymousUser):
                user_uwu = UwuUser.objects.get(user=user)
                for c in serializer.data:
                    readed_chapters = user_uwu.readed.all()
                    if c['url'].obj in readed_chapters:
                        c['isReaded'] = True
                    else:
                        c['isReaded'] = False
                
        return Response(serializer.data)
        
        
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get infromation of the manga.
        """
        super_retrieve = super().retrieve(request, *args, **kwargs)
        
        chapters = super_retrieve.data['chapters']
        
        if isinstance(request.user, AnonymousUser):
            return super_retrieve

        user = self.request.user
        user_uwu = UwuUser.objects.get(user=user)
        

        progress = 0
        
        if len(chapters) > 0:
            for c in chapters:
                readed_chapters = user_uwu.readed.all()
                if c.obj in readed_chapters:
                    progress += 1
                    
            progress = progress*100/len(chapters)
        
        super_retrieve.data['progress'] = progress
        favorites = user_uwu.favorites.all()
        super_retrieve.data['isFavorite'] = super_retrieve.data['url'].obj in favorites
        
        return super_retrieve

    def list(self, request):
        """
        Get all manga's info.
        """
        super_list = super().list(request)
        
        if isinstance(request.user, AnonymousUser):
            return super_list

        user = self.request.user
        user_uwu = UwuUser.objects.get(user=user)
        
        for r in super_list.data['results']:
            progress = 0
            if len(r['chapters']):
                chapters = user_uwu.readed.all()
                for c in r['chapters']:
                    if c.obj in chapters:
                        progress += 1
                progress = progress*100/len(r['chapters'])
            
            r['progress'] = progress
            
            favorites = user_uwu.favorites.all()
            r['isFavorite'] = r['url'].obj in favorites     

        return super_list
    
    @action(methods=['post'], detail=True)
    def add_remove_fav(self, request, pk=None):
        """
        Add or remove the manga to the current user.
        """
        user = request.user
        user_uwu = UwuUser.objects.get(user=request.user)
        manga = Manga.objects.get(pk=pk)
        
        if not user_uwu.is_fav(manga):
            user_uwu.favorites.add(manga)
            return Response({'status':f'The manga has been added to the {user}\'s favorites'}, status=status.HTTP_200_OK)
        else:
            user_uwu.favorites.remove(manga)
            return Response({'status':f'The manga has removed added from the {user}\'s favorites'}, status=status.HTTP_200_OK)

    
    
class ChapterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chapters to be viewed or edited.
    """
    queryset = Chapter.objects.all().order_by('order')
    serializer_class = ChapterSerializer
    permission_classes = [ChapterPermission,]

    def retrieve(self, request, *args, **kwargs):
        """
        Get infromation of the Chapter.
        """
        super_retrieve = super().retrieve(request, *args, **kwargs)
        
        if isinstance(request.user, AnonymousUser):
            return super_retrieve
        
        user_uwu = UwuUser.objects.get(user=request.user)
        
        if Chapter.objects.get(pk=super_retrieve.data['pk']) in user_uwu.readed.all():
            super_retrieve.data['isReaded'] = True
        else:
            super_retrieve.data['isReaded'] = False
        return super_retrieve
    
    @action(methods=['post'], detail=True)
    def add_remove_to_read(self, request, pk=None):
        """
        add or reamove the chapter in the user's readed chapter
        """
        
        user = User.objects.get(username=request.user)
        user_uwu = UwuUser.objects.get(user=user)
        
        chapter = Chapter.objects.get(pk=pk)
        
        if not user_uwu.is_readed(chapter):
            user_uwu.readed.add(chapter)
        
            return Response({'status':f'The chapter has been added to the {user}\'s readed chapter'}, status=status.HTTP_200_OK)
        else:
            user_uwu.readed.remove(chapter)
            return Response({'status':f'The chapter has been removed from the {user}\'s readed chapter'}, status=status.HTTP_200_OK)
        
        
        
    
class FriendRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chapters to be viewed or edited.
    """
    queryset = FriendRequest.objects.all().order_by('-timestamp')
    serializer_class = FriendRequestSerializer
    permission_classes = [FriendRequestPermission, ]
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        friend_request = FriendRequest(pk = pk)
        friend_request.decline()
        return Response({'status':'The friend request has been deleted'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        friend_request = FriendRequest(pk = pk)
        friend_request.cancel()
        return Response({'status':'The friend request has been canceled'})
        
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """
        Accept a friend request
        """
        try:
            friend_request = FriendRequest.objects.get(pk = pk)
        except:
            return Response({
                                'status' : 'Friend request does not exist',
                            },
                            status=status.HTTP_400_BAD_REQUEST)
        
        if not friend_request.is_on_hold:
            return Response({
                                'status' : 'Friend request has expired',
                            },
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(username=request.user)
        receiver = friend_request.receiver
        
        if not user == receiver:
            return Response({
                            'status' : 'You are not allowed to accept a friend request that does not concern you',
                            },
                            status=status.HTTP_401_UNAUTHORIZED) 
        
        sender = friend_request.sender
    
        UwuUser.objects.get(user=receiver).add_friend(sender)
        UwuUser.objects.get(user=sender).add_friend(receiver)
        friend_request.is_on_hold = False
        
        friend_request.save()
        
        return Response({
                            'status' : 'Friend request has been accepted',
                        },
                        status=status.HTTP_202_ACCEPTED)
    
    def list(self, request):
        """
        Get every friends requests in wich you are involve.
        """
        context = {'request':request}
        queryset = self.queryset.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        serializer = FriendRequestSerializer(queryset, many=True, context=context)
        
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False)
    def get_active_friend_request(self, request):
        """
        Get every friends requests that are adressed to you.
        """
        
        user = request.user
        
        friend_requests = FriendRequest.objects.all().filter(receiver=user).filter(is_on_hold=True).order_by('-timestamp')

        page = self.paginate_queryset(friend_requests)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(friend_requests, many=True)
        return Response(serializer.data)