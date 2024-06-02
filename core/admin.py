from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import UserChangeForm, UserCreationForm
from core.models import User, FriendRequest

admin.site.site_header = "SocialNet Administration"


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password"),
            },
        ),
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "friends",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "friends",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("id",)


admin.site.register(User, CustomUserAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    model = FriendRequest
    list_display = ["id", "sender", "receiver", "status", "created_at"]


admin.site.register(FriendRequest, FriendRequestAdmin)
