from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.forms import UserAccountCreationForm, UserAccountChangeForm
from apps.users.models import UserAccount, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


@admin.register(UserAccount)
class UserAccountAdmin(UserAdmin):
    add_form = UserAccountCreationForm
    form = UserAccountChangeForm

    model = UserAccount

    list_display = (
        "email",
        "username",
        "is_superuser",
        "is_staff",
        "is_active",
        "last_login",
    )
    list_filter = ("is_superuser", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    inlines = (ProfileInline,)


admin.site.register(Profile)
