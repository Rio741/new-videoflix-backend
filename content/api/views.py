from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Video, Genre, WatchProgress, Watchlist
from .serializers import VideoSerializer, GenreSerializer, WatchProgressSerializer, WatchlistSerializer

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
