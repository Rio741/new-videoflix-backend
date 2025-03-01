import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Video
from .tasks import convert_480p, convert_720p, convert_1080p
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print(f"📢 post_save wurde ausgelöst! Created={created}")

    if created and instance.video_file:
        video_path = instance.video_file.path
        print(f"🎬 Neues Video gespeichert: {video_path}")

        # Überprüfen, ob die Datei existiert
        if os.path.exists(video_path):
            print(f"✅ Datei gefunden: {video_path}, starte Konvertierung...")

            # Job zur Queue hinzufügen
            queue = django_rq.get_queue('default', autocommit=True)
            print("🔧 Füge Jobs zur Queue hinzu...")
            queue.enqueue(convert_480p, video_path)
            queue.enqueue(convert_720p, video_path)
            queue.enqueue(convert_1080p, video_path)
            print("🔧 Jobs zur Queue hinzugefügt.")
        else:
            print(f"❌ Fehler: Datei {video_path} existiert nicht!")


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print('📌 Video wurde gelöscht!')
    if instance.video_file:
        try:
            # Lösche die Originaldatei
            original_path = instance.video_file.path
            if os.path.isfile(original_path):
                os.unlink(original_path)
                print(f"🗑️ Originaldatei gelöscht: {original_path}")
        except Exception as e:
            print(f"❌ Fehler beim Löschen der Originaldatei: {e}")

        # Lösche auch die konvertierten Versionen, falls vorhanden
        for resolution in ["480p", "720p", "1080p"]:
            try:
                converted_path = instance.video_file.path.replace(".mp4", f"_{resolution}.mp4")
                if os.path.isfile(converted_path):
                    os.unlink(converted_path)
                    print(f"🗑️ Gelöschte konvertierte Datei: {converted_path}")
            except Exception as e:
                print(f"❌ Fehler beim Löschen der konvertierten Datei {resolution}: {e}")
