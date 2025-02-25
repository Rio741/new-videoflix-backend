from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from content_app.models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.forms import CheckboxSelectMultiple

class CustomUserAdmin(UserAdmin):
    list_display = ("email", "is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Berechtigungen", {"fields": ("is_staff", "is_superuser", "is_active")}),
        ("Wichtige Daten", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')
    search_fields = ('title',)
    formfield_overrides = {
        Video.genres.field: {'widget': CheckboxSelectMultiple}  # Genres als Checkboxen
    }

# class VideoResource(resources.ModelResource):
    
#     class META:
#         model = Video
        
# @admin.register(Video)
# class VideoAdmin(ImportExportModelAdmin):
#     pass