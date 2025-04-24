import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from .tasks import convert_to_hls
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Triggers HLS conversion when a new video is uploaded.

    Enqueues the video file for background processing using django_rq.
    """
    if created and instance.video_file:
        video_path = instance.video_file.path
        print(f"🎬 New video saved: {video_path}")

        if os.path.exists(video_path):
            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(convert_to_hls, instance.id, video_path)
            print("🚀 HLS conversion task has been enqueued.")
        else:
            print(f"❌ File not found: {video_path}")
