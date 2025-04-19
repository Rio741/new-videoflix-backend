# 🎬 Videoflix – Deine eigene Video-Plattform

Videoflix ist eine Streaming-Plattform, die es erlaubt, Videos hochzuladen, zu streamen und den Fortschritt beim Schauen zu speichern.  
Das Projekt wurde mit Django umgesetzt und nutzt Docker, Redis und PostgreSQL im Hintergrund.

---

## 🚀 Features

- Benutzer-Registrierung & Login mit E-Mail-Verifizierung
- Video-Upload (inkl. Verarbeitung & HLS-Streaming)
- Fortschritts-Speicherung beim Anschauen
- Hintergrundverarbeitung via RQ Worker
- REST-API (z. B. für das Frontend oder externe Clients)
- Dockerisierte Umgebung für einfache Entwicklung und Deployment

---

## 🐳 Start mit Docker (empfohlen)

1. Projekt klonen:
   ```bash
   git clone https://github.com/dein-name/videoflix.git
   cd videoflix
