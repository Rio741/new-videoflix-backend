from django.contrib import admin
from content_app.models import Video
from django.forms import CheckboxSelectMultiple

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')
    search_fields = ('title',)
    exclude = ('hls_master_playlist',)
    formfield_overrides = {
        Video.genres.field: {'widget': CheckboxSelectMultiple}
    }
