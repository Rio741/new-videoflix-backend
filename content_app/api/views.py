from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Video, Genre, WatchProgress, Watchlist, Genre
from .serializers import VideoSerializer, GenreSerializer, WatchProgressSerializer, WatchlistSerializer, GenreSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all().order_by("-upload_date")
    serializer_class = VideoSerializer

class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class WatchProgressView(generics.ListCreateAPIView):
    queryset = WatchProgress.objects.all()
    serializer_class = WatchProgressSerializer
    permission_classes = [IsAuthenticated]

class WatchlistView(generics.ListCreateAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

class VideosByGenreAPIView(APIView):
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
