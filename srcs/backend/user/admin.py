from django.contrib import admin
from user.models import User42

@admin.register(User42)
class AdminUsers(admin.ModelAdmin):
    list_display = ('username', 'creation', 'is_connected', 'is_active', 'is_staff', 'is_superuser')
 