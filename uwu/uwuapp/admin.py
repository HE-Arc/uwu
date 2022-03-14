from django.contrib import admin
from uwu.uwuapp.models import Chapter, FriendRequest, Manga, Readed, UwuUser

admin.site.register(UwuUser)
admin.site.register(Manga)
admin.site.register(Chapter)
admin.site.register(FriendRequest)
admin.site.register(Readed)