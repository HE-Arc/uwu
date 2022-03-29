from unittest import result
from PIL import Image
from django.contrib.auth.models import User
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from uwu.uwuapp import serializers
from uwu.uwuapp.serializers import ChapterSerializer, FriendRequestSerializer, UwuUserSerializer, MangaSerializer, UserSerializer
from uwu.uwuapp.models import Chapter, FriendRequest, Manga, UwuUser
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser

class UwuUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UwuUser.objects.all().order_by('pk')
    serializer_class = UwuUserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)           
    search_fields = ['user__username',] 
    

    @action(detail=True, methods=['post'])
    def unfriend(self, request, pk=None):
        """
        Unfriendinmg someone from the 'friends'
        """       

        user_uwu = UwuUser.objects.get(pk=pk)
        other_user = UwuUser.objects.get(user=request.data['other_user'])
        
        if user_uwu.is_friend(other_user):
            user_uwu.remove_friend(other_user.user)
            other_user.remove_friend(user_uwu.user)
            return Response({
                                'status' : f'{user_uwu} and {other_user} are not friend anymore',
                            }, 
                            status=status.HTTP_200_OK)
        else:
            return Response({
                                'status' : f'{user_uwu} and {other_user} are already not friend',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permissions_class = [permissions.IsAdminUser,]

    
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
    
    @action(detail=True)        
    def get_friends(self, request, pk=None):
        context = {'request':request}
        user = User.objects.get(pk=pk)
        uwu_user = UwuUser.objects.get(user=user)
        results = uwu_user.friends.all()
        serializer = UserSerializer(results, many=True, context=context)
        if len(serializer.data) > 0:
            for f in serializer.data:
                f['image'] = UwuUser.objects.get(user=f['url'].obj).image.url
        

        return Response(serializer.data)

    @action(detail=True)        
    def get_readed(self, request, pk=None):
        context = {'request':request}
        user = User.objects.get(pk=pk)
        uwu_user = UwuUser.objects.get(user=user)
        results = uwu_user.readed.all()
        serializer = ChapterSerializer(results, many=True, context=context)
        

        return Response(serializer.data)

    @action(detail=True)        
    def get_favorites(self, request, pk=None):
        context = {'request':request}
        user = User.objects.get(pk=pk)
        uwu_user = UwuUser.objects.get(user=user)
        results = uwu_user.favorites.all()
        serializer = MangaSerializer(results, many=True, context=context)
        

        return Response(serializer.data)
        
    
    
class MangaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mangas to be viewed or edited.
    """
    queryset = Manga.objects.all().order_by('-updated')
    serializer_class = MangaSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['is_finished']
    search_fields = ['name', 'author']
    ordering_fields = ['name', 'author', 'date']
    

    @action(detail=True)
    def get_chapters(self, request, pk=None):
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

    def retrieve(self, request, *args, **kwargs):
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
        '''
        add or reamove the chapter in the user's readed chapter
        '''
        
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
    queryset = FriendRequest.objects.all().order_by('-timestamp')
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated ]
    
    def create(self, request):
        sender = User.objects.get(username=request.user)
        
        try:
            receiver = User.objects.get(pk = request.data['other_user'])
        except:
            receiver = User.objects.get(username = request.data['other_user'])
        
        if sender == receiver:
            return Response({
                                'status' : 'You can\'t send a friend request to yourself',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
           
        sender_uwu = UwuUser.objects.get(user = sender)    
        if sender_uwu.is_friend(receiver):
            return Response({
                                'status' : f'{sender} and {receiver} are already friend',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        same_request = FriendRequest.objects.all().filter(sender = sender, receiver = receiver, is_on_hold=True)
        reverse_request = FriendRequest.objects.all().filter(sender = receiver, receiver = sender, is_on_hold=True)
        
        if same_request.count() > 0:
            return Response({
                                'status' : 'the same request already exist',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        if reverse_request.count() > 0:
            return Response({
                                'status' : f'{receiver} has already send a request to {sender}',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        FriendRequest.objects.create(sender=sender, receiver=receiver)
        return Response({
                            'status' : 'Friend request has been send',
                        },
                        status=status.HTTP_201_CREATED)
        
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """
        Accept a friend request
        Update both 'sender' and 'receiver' 'friends' field
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


    def get_queryset(self):
        queryset = self.queryset.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        return queryset
    
    @action(detail=False)
    def get_active_friend_request(self, request):
        
        user = User.objects.get(username=request.user)
        
        friend_requests = FriendRequest.objects.all().filter(receiver=user).order_by('-timestamp')

        page = self.paginate_queryset(friend_requests)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(friend_requests, many=True)
        return Response(serializer.data)