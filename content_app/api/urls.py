from django.urls import path
from .views import GenreListView, VideoListView, VideoDetailView, WatchProgressView, WatchlistView, VideosByGenreAPIView, StartedVideosAPIView

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("videos/", VideoListView.as_view(), name="video-list"),
    path("videos/<int:pk>/", VideoDetailView.as_view(), name="video-detail"),
    path("watch-progress/", WatchProgressView.as_view(), name="watch-progress"),
    path("watch-progress/<int:video_id>/", WatchProgressView.as_view(), name="get-watch-progress"),
    path("watchlist/", WatchlistView.as_view(), name="watchlist"),
    path("videos-by-genre/", VideosByGenreAPIView.as_view(), name="videos-by-genre"),
    path("started-videos/", StartedVideosAPIView.as_view(), name="started-videos"),
]
