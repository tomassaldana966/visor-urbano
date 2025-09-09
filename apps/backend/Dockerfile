FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat-openbsd \
    libffi-dev \
    libxml2 \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libcairo2 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN chmod +x docker-startup.sh

COPY docker-backend.sh wait-for-db.sh /app/
RUN chmod +x /app/docker-backend.sh /app/wait-for-db.sh

CMD ["./docker-startup.sh"]
