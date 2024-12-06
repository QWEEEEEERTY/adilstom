FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src
COPY run.sh /app


EXPOSE 8000


RUN chmod +x /app/run.sh
CMD ["source", "/app/run.sh"]
