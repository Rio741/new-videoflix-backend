FROM python:3

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "videoflix.wsgi:application", "--bind", "0.0.0.0:8000"]