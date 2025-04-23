#  Videoflix – Deine eigene Video-Plattform

Videoflix ist eine Streaming-Plattform, die es erlaubt, Videos hochzuladen, zu streamen und den Fortschritt beim Schauen zu speichern.  
Das Projekt wurde mit **Django** umgesetzt und nutzt **Docker**, **Redis** und **PostgreSQL** im Hintergrund.

> 🔗 **Live-Demo:** [https://web.videoflix.rio-stenger.de]
> *(Frontend und Backend sind online und verbunden.)*

---

## 🚀 Features

- 🔐 Benutzerregistrierung & Login mit E-Mail-Verifizierung
- 📹 Video-Upload inkl. automatischer Verarbeitung & HLS-Streaming
- 📊 Fortschritts-Speicherung beim Anschauen
- 🔁 Hintergrundjobs mit RQ (z. B. für Video-Konvertierung)
- 🔌 Vollständige REST-API für Integration mit Frontend oder Clients
- 🐳 Dockerisierte Umgebung für Entwicklung & Deployment
- ✅ Tests mit `pytest` und `coverage.py` implementiert

---

## 🛠️ Technologien

- **Backend:** Django, Django REST Framework
- **Task-Queue:** Redis + Django-RQ
- **Datenbank:** PostgreSQL
- **Containerisierung:** Docker, Docker Compose
- **Tests:** Pytest, Coverage.py
- **Deployment:** Docker-Setup auf V-Server (Ubuntu)

---

## 🧪 **Testabdeckung:**  
- ![Coverage Screenshot](assets/test_coverage.png)  
- Aktuell bei **88 %** – Ziel: 80 %+