from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'display_name', 'is_staff')
    search_fields = ('email', 'display_name')
    ordering = ('email',)
    filter_horizontal = ()
