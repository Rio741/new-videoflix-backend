from rest_framework import serializers
from ..models import Video, Genre, WatchProgress, Watchlist
from django.shortcuts import get_object_or_404


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Genre model.

    Serializes the 'id' and 'name' fields of a genre.
    """
    class Meta:
        model = Genre
        fields = ["id", "name"]


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.

    Includes nested Genre serialization to display all genres related to a video.
    """
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "description",
            "upload_date",
            "thumbnail",
            "video_file",
            "genres",
            "hls_master_playlist"
        ]


class WatchProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for tracking a user's watch progress on a video.

    - 'video_id' is required for identifying the video (write-only).
    - 'progress' maps to the 'timestamp' field on the model.
    """
    video_id = serializers.IntegerField(write_only=True)
    progress = serializers.FloatField(source="timestamp", min_value=0)

    class Meta:
        model = WatchProgress
        fields = ["id", "video_id", "progress", "updated_at"]

    def create(self, validated_data):
        """
        Creates or updates the watch progress for a specific user and video.

        Args:
            validated_data (dict): Contains the video ID and progress timestamp.
        """
        video_id = validated_data.pop("video_id")
        user = self.context["request"].user
        video = get_object_or_404(Video, id=video_id)

        progress, created = WatchProgress.objects.update_or_create(
            user=user,
            video=video,
            defaults=validated_data
        )
        return progress


class WatchlistSerializer(serializers.ModelSerializer):
    """
    Serializer for the Watchlist model.

    Serializes the relationship between users and the videos they added to their watchlist.
    """
    class Meta:
        model = Watchlist
        fields = ["id", "user", "video", "added_at"]
