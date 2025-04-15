# Base image: official Jenkins LTS
FROM jenkins/jenkins:lts

# Switch to root user to install packages
USER root

# Install Python, pip, venv, and other essential tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# (Optional) Upgrade pip
RUN python3 -m pip install --upgrade pip

# Switch back to Jenkins user for security
USER jenkins