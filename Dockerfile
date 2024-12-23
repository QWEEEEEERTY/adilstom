FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y make \
    && apt-get install -y netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000


RUN chmod +x /app/wait-for-db.sh
ENTRYPOINT ["/app/wait-for-db.sh"]
