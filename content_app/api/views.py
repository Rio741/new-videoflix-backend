from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Video, Genre, WatchProgress, Watchlist
from .serializers import VideoSerializer, GenreSerializer, WatchProgressSerializer, WatchlistSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class GenreListView(generics.ListAPIView):
    """
    API endpoint to retrieve the list of all available genres.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class VideoListView(generics.ListAPIView):
    """
    API endpoint to retrieve the list of all videos, ordered by upload date (newest first).
    """
    queryset = Video.objects.all().order_by("-upload_date")
    serializer_class = VideoSerializer


class VideoDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve the details of a single video by ID.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class WatchProgressView(APIView):
    """
    API endpoint for tracking and retrieving watch progress for a video.

    - POST: Updates or creates the watch progress.
    - GET: Retrieves the current watch progress for a specific video.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Update or create watch progress for a user and video.
        """
        video_id = request.data.get("video_id")
        timestamp = request.data.get("timestamp")

        if not video_id or timestamp is None:
            return Response({"error": "Missing data"}, status=400)

        video = get_object_or_404(Video, id=video_id)

        progress, created = WatchProgress.objects.update_or_create(
            user=request.user,
            video=video,
            defaults={"timestamp": timestamp}
        )

        return Response({"progress": progress.timestamp if progress is not None else 0}, status=200)

    def get(self, request, video_id):
        """
        Retrieve watch progress for the current user and a specific video.
        """
        progress = WatchProgress.objects.filter(user=request.user, video_id=video_id).first()

        if not progress:
            return Response({"progress": 0}, status=200)

        return Response({"progress": progress.timestamp}, status=200)


class WatchlistView(generics.ListCreateAPIView):
    """
    API endpoint to retrieve or add videos to the authenticated user's watchlist.
    """
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]


class VideosByGenreAPIView(APIView):
    """
    API endpoint to retrieve videos grouped by genre.
    """
    def get(self, request):
        genres = Genre.objects.prefetch_related('videos').all()
        data = []

        for genre in genres:
            videos = Video.objects.filter(genres=genre)
            video_data = VideoSerializer(videos, many=True).data
            data.append({
                "genre": GenreSerializer(genre).data,
                "videos": video_data
            })

        return Response(data)


class StartedVideosAPIView(APIView):
    """
    API endpoint to retrieve videos that the user has started watching
    (i.e., progress greater than 5 seconds).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        started_videos = WatchProgress.objects.filter(
            user=request.user,
            timestamp__gt=5
        ).select_related('video')

        videos = [progress.video for progress in started_videos]
        video_data = VideoSerializer(videos, many=True).data

        return Response(video_data)