FROM --platform=linux/amd64 python:3.7-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# Configure APT to handle mirror issues and install system dependencies
RUN echo 'Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries && \
    echo 'Acquire::http::Timeout "120";' >> /etc/apt/apt.conf.d/80-retries && \
    echo 'Acquire::Check-Valid-Until "false";' >> /etc/apt/apt.conf.d/80-retries && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* && \
    apt-get clean && \
    apt-get update --allow-releaseinfo-change -o Acquire::Check-Valid-Until=false || \
    (sleep 5 && apt-get update --allow-releaseinfo-change -o Acquire::Check-Valid-Until=false) && \
    apt-get install -y --no-install-recommends \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    || apt-get install -y --no-install-recommends --allow-unauthenticated \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port for Flask server
EXPOSE 4567

# Set working directory
WORKDIR /app

# Default command (can be overridden)
CMD ["python", "testSimulation.py"]
