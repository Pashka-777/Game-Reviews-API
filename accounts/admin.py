from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email','first_name','last_name','is_staff','is_verified')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Personal', {'fields': ('first_name','last_name','bio','profile_image')}),
        ('Security', {'fields': ('is_verified','recovery_question')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1','password2'),
        }),
    )
