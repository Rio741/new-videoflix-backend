import os
import subprocess
import logging
from django_rq import job
from content_app.models import Video


FFMPEG_PATH = "/usr/bin/ffmpeg"

logging.basicConfig(level=logging.INFO)


@job
def convert_to_hls(video_id, source):
    """
    Converts a video to HLS format (.m3u8 + .ts segments)
    """
    if not os.path.exists(source):
        logging.error(f"❌ Fehler: Datei {source} existiert nicht!")
        return
    
    filename, ext = os.path.splitext(os.path.basename(source))
    target_dir = os.path.join(os.path.dirname(source), f"{filename}_hls")
    os.makedirs(target_dir, exist_ok=True)

    master_playlist = os.path.join(target_dir, "master.m3u8")

    cmd = [
        FFMPEG_PATH, "-i", source, "-preset", "fast", "-g", "48", "-sc_threshold", "0",

        "-map", "0:v:0", "-map", "0:a:0?", "-b:v:0", "500k", "-s:v:0", "854x480",
        "-c:v:0", "libx264", "-crf", "20", "-c:a:0", "aac", "-b:a:0", "128k",
        "-f", "hls", "-hls_time", "6", "-hls_playlist_type", "vod",
        "-hls_segment_filename", f"{target_dir}/480p_%03d.ts", f"{target_dir}/480p.m3u8",

        "-map", "0:v:0", "-map", "0:a:0?", "-b:v:1", "1000k", "-s:v:1", "1280x720",
        "-c:v:1", "libx264", "-crf", "20", "-c:a:1", "aac", "-b:a:1", "128k",
        "-f", "hls", "-hls_time", "6", "-hls_playlist_type", "vod",
        "-hls_segment_filename", f"{target_dir}/720p_%03d.ts", f"{target_dir}/720p.m3u8",

        "-map", "0:v:0", "-map", "0:a:0?", "-b:v:2", "2000k", "-s:v:2", "1920x1080",
        "-c:v:2", "libx264", "-crf", "20", "-c:a:2", "aac", "-b:a:2", "128k",
        "-f", "hls", "-hls_time", "6", "-hls_playlist_type", "vod",
        "-hls_segment_filename", f"{target_dir}/1080p_%03d.ts", f"{target_dir}/1080p.m3u8",

        "-var_stream_map", "v:0,a:0 v:1,a:1 v:2,a:2",
        "-f", "hls"
    ]

    try:
        subprocess.run(cmd, check=True)
        logging.info(f"✅ HLS-Konvertierung abgeschlossen: {target_dir}")

        master_playlist_content = """#EXTM3U
            #EXT-X-STREAM-INF:BANDWIDTH=500000,RESOLUTION=854x480
            480p.m3u8
            #EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=1280x720
            720p.m3u8
            #EXT-X-STREAM-INF:BANDWIDTH=2000000,RESOLUTION=1920x1080
            1080p.m3u8
            """
        with open(master_playlist, "w") as f:
            f.write(master_playlist_content)

        logging.info(f"✅ Master-Playlist erstellt: {master_playlist}")

        video = Video.objects.get(id=video_id)
        video.hls_master_playlist = f"videos/{filename}_hls/master.m3u8"
        video.save()
        logging.info(f"✅ Video-Datenbank aktualisiert: {video.hls_master_playlist}")

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Fehler bei der HLS-Konvertierung: {e}")