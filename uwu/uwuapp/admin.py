from django.contrib import admin
from uwu.uwuapp.models import Chapter, HasRead, IsFriend, Manga

# Register your models here.
admin.site.register(Manga)
admin.site.register(Chapter)
admin.site.register(IsFriend)
admin.site.register(HasRead)