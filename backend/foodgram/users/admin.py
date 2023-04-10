from django.contrib import admin

from .models import User

FIELDS = ('email', 'username', 'last_name', 'first_name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = FIELDS
    list_filter = FIELDS
    search_fields = FIELDS
