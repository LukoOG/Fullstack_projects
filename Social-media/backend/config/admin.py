from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from posts.models import *

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to be used in displaying the User model.
    list_display = ('email', 'first_name', 'last_name', 'username', 'phone_number', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('-date_joined',)

    # Fieldsets for viewing/editing a user in admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'bio', 'location', 'website', 'profile_pic', 'username', 'phone_number', 'follows')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Fieldsets for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'phone_number', 'follows', 'password1', 'password2'),
        }),
    )
    
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)