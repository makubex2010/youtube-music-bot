FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

CMD ["python", "main.py"]
