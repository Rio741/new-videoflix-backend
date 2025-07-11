from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel configuration for the User model.
    """
    list_display = ("email", "is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Berechtigungen", {"fields": ("is_staff", "is_superuser", "is_active")}),
        ("Wichtige Daten", {"fields": ("last_login",)}),
    )

    readonly_fields = ("date_joined", "last_login")

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )

admin.site.register(User, CustomUserAdmin)
