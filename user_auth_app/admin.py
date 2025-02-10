from django.contrib import admin
from profiles.api.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "type")


admin.site.register(
    UserProfile,
    UserProfileAdmin,
)
