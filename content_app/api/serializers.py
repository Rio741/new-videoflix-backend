from rest_framework import serializers
from ..models import Video, Genre, WatchProgress, Watchlist
from django.shortcuts import get_object_or_404


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class VideoSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ["id", "title", "description", "upload_date", "thumbnail", "video_file", "genres", "hls_master_playlist"]


class WatchProgressSerializer(serializers.ModelSerializer):
    video_id = serializers.IntegerField(write_only=True)
    progress = serializers.FloatField(source="timestamp", min_value=0)

    class Meta:
        model = WatchProgress
        fields = ["id", "video_id", "progress", "updated_at"]

    def create(self, validated_data):
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
    class Meta:
        model = Watchlist
        fields = ["id", "user", "video", "added_at"]

