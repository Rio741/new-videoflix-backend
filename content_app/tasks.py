import os
import subprocess
import logging
from django_rq import job
from content_app.models import Video

FFMPEG_PATH = "/usr/bin/ffmpeg"

logging.basicConfig(level=logging.INFO)

@job
def convert_to_hls(video_id, source):
    import shutil

    if not os.path.exists(source):
        logging.error(f"❌ Fehler: Datei {source} existiert nicht!")
        return

    filename, ext = os.path.splitext(os.path.basename(source))
    target_dir = os.path.join(os.path.dirname(source), f"{filename}_hls")
    os.makedirs(target_dir, exist_ok=True)

    output_path = os.path.join(target_dir, "master.m3u8")

    cmd = [
        FFMPEG_PATH, "-i", source, "-preset", "fast", "-g", "48", "-sc_threshold", "0",

        # Video- und Audiostreams für die verschiedenen Auflösungen definieren
        "-map", "0:v:0", "-map", "0:a:0",    # 480p
        "-map", "0:v:0", "-map", "0:a:0",    # 720p
        "-map", "0:v:0", "-map", "0:a:0",    # 1080p

        # Video-Settings
        "-s:v:0", "854x480", "-b:v:0", "500k",
        "-s:v:1", "1280x720", "-b:v:1", "1000k",
        "-s:v:2", "1920x1080", "-b:v:2", "2000k",

        "-c:v", "libx264", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k",

        "-var_stream_map", "v:0,a:0 v:1,a:1 v:2,a:2",
        "-f", "hls",
        "-hls_time", "6",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", os.path.join(target_dir, "v%v/segment_%03d.ts"),
        os.path.join(target_dir, "v%v/prog.m3u8")
    ]

    try:
        subprocess.run(cmd, check=True)
        logging.info(f"✅ HLS-Konvertierung abgeschlossen: {target_dir}")

        # ➕ Master Playlist Pfad eintragen
        video = Video.objects.get(id=video_id)
        video.hls_master_playlist = f"videos/{filename}_hls/master.m3u8"
        video.save()
        logging.info(f"✅ Video-Datenbank aktualisiert: {video.hls_master_playlist}")

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Fehler bei der HLS-Konvertierung: {e}")
