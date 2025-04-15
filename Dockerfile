FROM python:3.9-slim

# Make sure we are root
USER root

# Avoid prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Optional: run preprocessing or pipeline
RUN python pipeline/pipeline.py

# Expose port
EXPOSE 8000

# Start app
CMD ["python", "app/server/app.py"]