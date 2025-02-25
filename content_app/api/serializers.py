from rest_framework import serializers
from ..models import Video, Genre, WatchProgress, Watchlist

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]

class VideoSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ["id", "title", "description", "upload_date", "thumbnail", "video_file_1080p", "video_file_720p", "video_file_360p", "genres"]

class WatchProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchProgress
        fields = ["id", "user", "video", "timestamp", "updated_at"]

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ["id", "user", "video", "added_at"]