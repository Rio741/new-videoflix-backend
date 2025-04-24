from django.contrib import admin
from content_app.models import Video
from django.forms import CheckboxSelectMultiple


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the Video model.

    - Displays video title and upload date in the list view.
    - Enables search functionality by video title.
    - Excludes the HLS master playlist field from the form.
    - Uses checkbox widgets for genre selection (many-to-many field).
    """
    list_display = ('title', 'upload_date')
    search_fields = ('title',)
    exclude = ('hls_master_playlist',)
    formfield_overrides = {
        Video.genres.field: {'widget': CheckboxSelectMultiple}
    }
