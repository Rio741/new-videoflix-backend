from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Genre, Video, WatchProgress, Watchlist
from rest_framework.test import APITestCase
from content_app.api.serializers import GenreSerializer, VideoSerializer, WatchlistSerializer


class GenreModelTest(TestCase):
    def test_create_genre(self):
        genre = Genre.objects.create(name="Action")
        self.assertEqual(genre.name, "Action")
        self.assertEqual(str(genre), "Action")

class VideoModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password")
        self.genre = Genre.objects.create(name="Action")
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            thumbnail="test_thumbnail.jpg",
            video_file="test_video.mp4"
        )
        self.video.genres.add(self.genre)

    def test_video_creation(self):
        video = self.video
        self.assertEqual(video.title, "Test Video")
        self.assertEqual(video.description, "Test Description")
        self.assertTrue(video.thumbnail)
        self.assertTrue(video.video_file)
        self.assertEqual(video.genres.count(), 1)

class WatchProgressModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password")
        self.genre = Genre.objects.create(name="Action")
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            thumbnail="test_thumbnail.jpg",
            video_file="test_video.mp4"
        )
        self.watch_progress = WatchProgress.objects.create(
            user=self.user,
            video=self.video,
            timestamp=120.5
        )

    def test_watch_progress_creation(self):
        progress = self.watch_progress
        self.assertEqual(progress.user, self.user)
        self.assertEqual(progress.video, self.video)
        self.assertEqual(progress.timestamp, 120.5)

    def test_watch_progress_save_negative_timestamp(self):
        self.watch_progress.timestamp = -50
        self.watch_progress.save()
        self.assertEqual(self.watch_progress.timestamp, 0)

class WatchlistModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password")
        self.genre = Genre.objects.create(name="Action")
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            thumbnail="test_thumbnail.jpg",
            video_file="test_video.mp4"
        )
        self.watchlist = Watchlist.objects.create(
            user=self.user,
            video=self.video
        )

    def test_watchlist_creation(self):
        watchlist_item = self.watchlist
        self.assertEqual(watchlist_item.user, self.user)
        self.assertEqual(watchlist_item.video, self.video)

class GenreSerializerTest(APITestCase):
    def test_genre_serializer(self):
        genre = Genre.objects.create(name="Action")
        serializer = GenreSerializer(genre)
        self.assertEqual(serializer.data['name'], "Action")

class VideoSerializerTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password")
        self.genre = Genre.objects.create(name="Action")
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            thumbnail="test_thumbnail.jpg",
            video_file="test_video.mp4"
        )
        self.video.genres.add(self.genre)

    def test_video_serializer(self):
        serializer = VideoSerializer(self.video)
        self.assertEqual(serializer.data['title'], "Test Video")
        self.assertEqual(len(serializer.data['genres']), 1)

class WatchlistSerializerTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password")
        self.genre = Genre.objects.create(name="Action")
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            thumbnail="test_thumbnail.jpg",
            video_file="test_video.mp4"
        )
        self.watchlist = Watchlist.objects.create(
            user=self.user,
            video=self.video
        )

    def test_watchlist_serializer(self):
        serializer = WatchlistSerializer(self.watchlist)
        self.assertEqual(serializer.data['user'], self.user.id)
        self.assertEqual(serializer.data['video'], self.video.id)