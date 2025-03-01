import os
import subprocess
import logging
from django_rq import job

# Setze den richtigen FFmpeg-Pfad
FFMPEG_PATH = "/usr/bin/ffmpeg"

# Konfiguration für Logging
logging.basicConfig(level=logging.INFO)

@job  # Dekorator, damit diese Funktion als RQ-Task verwendet werden kann
def convert_video(source, resolution, height):
    """Generische Funktion zur Video-Konvertierung mit FFmpeg"""
    if not os.path.exists(source):
        logging.error(f"❌ Fehler: Datei {source} existiert nicht!")
        return

    if not os.path.exists(FFMPEG_PATH):
        logging.error(f"❌ FFmpeg wurde nicht gefunden unter: {FFMPEG_PATH}")
        return

    filename, ext = os.path.splitext(source)
    target = f"{filename}_{resolution}{ext}"

    cmd = [
        FFMPEG_PATH, "-i", source,
        "-vf", f"scale=-2:{height}",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac", "-strict", "-2",
        target
    ]

    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpeg_output = result.stdout.decode()
        ffmpeg_errors = result.stderr.decode()
        logging.info(f"✅ Konvertierung erfolgreich: {target}")
        logging.debug(f"FFmpeg Output: {ffmpeg_output}")
        logging.error(f"FFmpeg Errors: {ffmpeg_errors}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Fehler bei FFmpeg: {e}")
        if e.stderr:
            logging.error(f"FFmpeg Fehlerausgabe: {e.stderr.decode()}")

    return f"Video konvertiert: {target}"

# Spezifische Funktionen für jede Auflösung
def convert_480p(source):
    convert_video(source, "480p", 480)

def convert_720p(source):
    convert_video(source, "720p", 720)

def convert_1080p(source):
    convert_video(source, "1080p", 1080)
