# HTTPS Proxy Server

A robust HTTPS proxy server built with mitmproxy that automatically maintains a pool of working proxies from GitHub sources.

## 🚀 Features

- **Automatic Proxy Pool Management**: Fetches and updates proxy list from GitHub every 5 minutes
- **Health Check System**: Continuously validates proxy availability against target websites
- **Real-time Monitoring**: Web interface to monitor proxy requests and traffic
- **SSL/TLS Support**: Full HTTPS interception with certificate management
- **Docker Support**: Easy deployment with Docker and docker-compose
- **Thread-safe Operations**: Concurrent proxy testing and management

## 📁 Project Structure

```
https_proxy_server/
├── proxy_manager.py      # Core proxy pool manager (fetching, testing, maintenance)
├── proxy_addon.py        # mitmproxy addon for request handling and monitoring
├── start_proxy.py        # Main application launcher
├── test_proxy.py         # Proxy testing utility
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker container configuration
├── docker-compose.yml   # Docker Compose configuration
├── .dockerignore       # Docker ignore file
├── start_chrome_proxy.sh # Chrome browser launcher with proxy settings
└── install_cert_manual.md # SSL certificate installation guide
```

## 🔧 Installation & Usage

### Option 1: Docker Deployment (Recommended) 🐳

#### Prerequisites
- Docker
- Docker Compose

#### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/claude89757/https_proxy_server.git
cd https_proxy_server
```

2. Start the proxy server using Docker Compose:
```bash
docker-compose up -d
```

3. View logs:
```bash
docker-compose logs -f
```

4. Stop the server:
```bash
docker-compose down
```

#### Docker Commands

Build the image:
```bash
docker build -t https-proxy-server .
```

Run without docker-compose:
```bash
docker run -d \
  --name https_proxy_server \
  -p 8080:8080 \
  -p 8081:8081 \
  -v mitmproxy_certificates:/root/.mitmproxy \
  https-proxy-server
```

#### Access Points
- **Proxy server**: `http://localhost:8080`
- **Web monitoring interface**: `http://localhost:8081`

#### Certificate Management in Docker

The mitmproxy certificates are stored in a Docker volume. To retrieve them:

```bash
# Copy certificates from container
docker cp https_proxy_server:/root/.mitmproxy/mitmproxy-ca-cert.pem ./

# Or access them from the volume
docker run --rm -v mitmproxy_certificates:/certs alpine cat /certs/mitmproxy-ca-cert.pem > mitmproxy-ca-cert.pem
```

### Option 2: Local Installation

#### Prerequisites
- Python 3.7+
- pip3

#### Setup

1. Clone the repository:
```bash
git clone https://github.com/claude89757/https_proxy_server.git
cd https_proxy_server
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Start the proxy server:
```bash
python3 start_proxy.py
```

#### Access Points
- **Proxy server**: `http://127.0.0.1:8080`
- **Web monitoring interface**: `http://127.0.0.1:8081`

## 🔐 SSL Certificate Setup

### For Docker Users

1. Start the container first to generate certificates:
```bash
docker-compose up -d
```

2. Extract the certificate:
```bash
docker cp https_proxy_server:/root/.mitmproxy/mitmproxy-ca-cert.pem ./
```

3. Install the certificate on your system:
   - **macOS**: Double-click the .pem file and add to System Keychain, then trust it
   - **Windows**: Import to Trusted Root Certification Authorities
   - **Linux**: Copy to `/usr/local/share/ca-certificates/` and run `update-ca-certificates`

### For Local Installation

Follow the instructions in `install_cert_manual.md` after first run.

## 🌐 Configure Your Browser

### Option A: Use Dedicated Chrome Instance
```bash
./start_chrome_proxy.sh
```

### Option B: Manual Browser Configuration
1. Set HTTP/HTTPS proxy to:
   - For Docker: `localhost:8080`
   - For Local: `127.0.0.1:8080`

### Option C: System Proxy Configuration
- **macOS**: System Settings → Network → Advanced → Proxies
- **Windows**: Settings → Network & Internet → Proxy
- **Linux**: Network Settings → Network Proxy

## 🧪 Testing

### Test with Docker:
```bash
# Run test from inside container
docker-compose exec https-proxy python3 test_proxy.py

# Or test from host
curl -x http://localhost:8080 https://httpbin.org/ip
```

### Test with Local Installation:
```bash
python3 test_proxy.py
```

## 🔄 How It Works

1. **Proxy Fetching**: `proxy_manager.py` retrieves proxy lists from GitHub repositories
2. **Validation**: Each proxy is tested against target websites for availability
3. **Local Proxy Server**: mitmproxy runs as a local proxy server on port 8080
4. **Request Routing**: Valid proxies are used to route your HTTP/HTTPS requests
5. **Monitoring**: `proxy_addon.py` tracks proxy usage and performance metrics

## ⚙️ Configuration

### Environment Variables (Docker)

You can customize the behavior by setting environment variables in `docker-compose.yml`:

```yaml
environment:
  - MITMPROXY_OPTS=--set confdir=/root/.mitmproxy
  - UPDATE_INTERVAL=300  # Proxy update interval in seconds
  - TEST_BATCH_SIZE=10   # Number of proxies to test per batch
```

### Configuration Parameters

- Update interval: 5 minutes (default)
- Test batch size: 10 proxies per batch
- Timeout settings for proxy validation
- Target URL for health checks

## 📊 Monitoring

Access the web interface at:
- Docker: `http://localhost:8081`
- Local: `http://127.0.0.1:8081`

Features:
- View real-time request logs
- Monitor proxy performance
- Check proxy pool status
- Debug connection issues

## 🐛 Troubleshooting

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs

# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

**Port conflicts:**
```bash
# Change ports in docker-compose.yml
ports:
  - "18080:8080"  # Use different host port
  - "18081:8081"
```

### Certificate Issues
- Ensure the mitmproxy certificate is properly installed in your system
- For Docker, make sure to extract and install the certificate from the container
- Restart browser after certificate installation

### No Available Proxies
- Check container logs: `docker-compose logs`
- Verify internet connectivity from container
- Check if GitHub API is accessible

## 🚀 Production Deployment

For production use, consider:

1. Using environment-specific configuration
2. Setting up proper logging volumes
3. Implementing health checks
4. Using a reverse proxy like nginx
5. Setting resource limits in docker-compose.yml:

```yaml
services:
  https-proxy:
    # ... other config ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Note**: This tool is for educational and testing purposes. Please ensure compliance with all applicable laws and terms of service when using proxy services.