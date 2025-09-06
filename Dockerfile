# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY proxy_manager.py .
COPY proxy_addon.py .
COPY start_proxy.py .
COPY test_proxy.py .

# Create directory for mitmproxy certificates
RUN mkdir -p /root/.mitmproxy

# Expose ports
# 8080: Proxy port
# 8081: Web interface port
EXPOSE 8080 8081

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MITMPROXY_OPTS=""

# Run the proxy server
CMD ["python3", "start_proxy.py"]