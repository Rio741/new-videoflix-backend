from django.urls import path
from .views import GenreListView, VideoListView, VideoDetailView, WatchProgressView, WatchlistView

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("videos/", VideoListView.as_view(), name="video-list"),
    path("videos/<int:pk>/", VideoDetailView.as_view(), name="video-detail"),
    path("watch-progress/", WatchProgressView.as_view(), name="watch-progress"),
    path("watchlist/", WatchlistView.as_view(), name="watchlist")
]
