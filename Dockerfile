FROM --platform=linux/amd64 python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . .

RUN pip install --no-cache-dir -e .

RUN python pipeline/pipeline.py

EXPOSE 8000

CMD ["python", "app/server/app.py"]