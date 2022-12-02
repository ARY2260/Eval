from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'email',
        'email_verified',
        'created_at',
        'updated_at',
    )

admin.site.register(User, UserAdmin)