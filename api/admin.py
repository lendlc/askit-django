from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import *

# Custom User Model on Admin Site
class CustomUserAdmin(UserAdmin):
    # fields to show, when making changes on specific record.
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (('Personal info'),
            {'fields': ('first_name', 'last_name', 'role',)
        }),
        (('Permissions'),
            {'fields': ('is_active','is_verified',)} #'is_superuser','groups', 'user_permissions'
        ),
    )

    # fields for user creation in admin site.
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'birth_date','password1', 'password2', 'role')
        }),
    )   

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    #Fields to show in List
    list_display = ('username', 'email','date_joined', 'role', 'last_login', 'is_verified', )
    list_filter = ('role', 'is_active', 'is_verified',)
    ordering = ('date_joined', )

#add models below.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Tutor,)