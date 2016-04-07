from django.contrib import admin
from .models import Task, UserProfile
from .forms import UserRegistrationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin

class UserProfileAdmin(UserAdmin):
    
    form = UserChangeForm
    add_form = UserRegistrationForm

    list_display = ['email', 'timezone', 'known_as', 'is_superuser', 'is_staff', 'is_active']
    list_filter = ['is_superuser', 'is_staff', 'is_active',]
    filter_horizontal = ()
    ordering = ('email',)
    fieldsets = (
                 (None, {'fields' : ('email', 'password')}),
                 ('Personal Info', {'fields' : ('timezone', 'known_as')})
                )

    add_fieldsets = (
                 (None, {'fields' : ('email', 'timezone', 'known_as', 'password1', 'password2')}),
                )

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Task)