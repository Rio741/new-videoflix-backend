from django.db import models
from django.contrib.auth import get_user_model


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def create_default_genres():
        default_genres = ["Action", "Drama", "Komödie", "Horror", "Sci-Fi", "Romantik", "Thriller", "Dokumentation"]
        for genre in default_genres:
            Genre.objects.get_or_create(name=genre)


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to="thumbnails/")
    video_file = models.FileField(upload_to="videos", blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="videos")
    hls_master_playlist = models.FileField(upload_to="hls/", blank=True, null=True)

    def __str__(self):
        return self.title


class WatchProgress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    timestamp = models.FloatField(
        help_text="Letzte Position im Video (in Sekunden)")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.video.title} ({self.timestamp}s)"


class Watchlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.video.title}"
