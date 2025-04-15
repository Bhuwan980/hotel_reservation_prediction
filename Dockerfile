FROM python:slim

# Don't write .pyc files and enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Ensure you're running commands as root to install packages
USER root

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy project files into container
COPY . .

# Install Python dependencies from setup.py
RUN pip install --no-cache-dir -e .

# Optional: Run your pipeline script during build (not always recommended in Dockerfile)
# You may want to move this to CMD or ENTRYPOINT depending on use case
RUN python pipeline/pipeline.py

# Expose the port your app runs on
EXPOSE 8000

# Start the application server
CMD ["python", "app/server/app.py"]