from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'bio')
    search_fields = ('user__username', 'name')

admin.site.register(CustomUser, UserAdmin)
