from pyexpat import model
from tabnanny import verbose
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from uwu.uwuapp.models import Chapter, Manga, UwuUser

class UwuUserInLine(admin.StackedInline):
    model = UwuUser
    can_delete = False
    verbose_name_plural = 'UwuUsers'

class UserAdmin(BaseUserAdmin):
    inlines = (UwuUserInLine,)

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Manga)
admin.site.register(Chapter)