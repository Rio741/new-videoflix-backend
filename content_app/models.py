from django.db import models
from django.contrib.auth import get_user_model


class Genre(models.Model):
    """
    Represents a video genre such as Action, Drama, Comedy, etc.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def create_default_genres():
        """
        Creates a predefined list of default genres if they do not already exist.
        """
        default_genres = ["Action", "Drama", "Comedy", "Horror", "Sci-Fi", "Romance", "Thriller", "Documentary"]
        for genre in default_genres:
            Genre.objects.get_or_create(name=genre)


class Video(models.Model):
    """
    Stores information about uploaded videos, including title, description,
    file path, genres, and HLS master playlist.
    """
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
    """
    Tracks how far a user has watched a specific video.
    Stores the timestamp in seconds.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    timestamp = models.FloatField(
        help_text="Last watched position in the video (in seconds)",
        default=0
    )
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Ensures that the timestamp cannot be negative.
        """
        if self.timestamp < 0:
            self.timestamp = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.video.title} ({self.timestamp}s)"


class Watchlist(models.Model):
    """
    Represents a user's watchlist by linking users to their saved videos.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.video.title}"