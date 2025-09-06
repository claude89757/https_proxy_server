# HTTPS Proxy Server

A robust HTTPS proxy server built with mitmproxy that automatically maintains a pool of working proxies from GitHub sources.

## 🚀 Features

- **Automatic Proxy Pool Management**: Fetches and updates proxy list from GitHub every 5 minutes
- **Health Check System**: Continuously validates proxy availability against target websites
- **Real-time Monitoring**: Web interface to monitor proxy requests and traffic
- **SSL/TLS Support**: Full HTTPS interception with certificate management
- **Docker Deployment**: Easy deployment with Docker and docker-compose
- **Thread-safe Operations**: Concurrent proxy testing and management

## 📁 Project Structure

```
https_proxy_server/
├── proxy_manager.py      # Core proxy pool manager
├── proxy_addon.py        # mitmproxy addon for request handling
├── start_proxy.py        # Main application launcher
├── tunnel_proxy.py       # HTTP CONNECT tunnel proxy implementation
├── start_tunnel_proxy.py # Tunnel proxy launcher (certificate-free)
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker container configuration
├── docker-compose.yml   # Docker Compose configuration
└── .dockerignore       # Docker ignore file
```

## ⚠️ Security Notice

**Important**: This proxy server is configured to accept connections from any IP address. This is necessary for cloud deployment but poses security risks. Please ensure:
- Use strong firewall rules to limit access
- Deploy in isolated network environments when possible
- Monitor access logs regularly
- Never expose sensitive internal networks through this proxy

## 🔧 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation

1. Clone the repository:
```bash
git clone https://github.com/claude89757/https_proxy_server.git
cd https_proxy_server
```

2. Start the proxy server:
```bash
docker-compose up -d
```

3. View logs:
```bash
docker-compose logs -f
```

### Access Points
- **Tunnel Proxy Server**: `http://<your-server-ip>:8080` (Certificate-free HTTPS proxying)
- **Web Interface**: `http://<your-server-ip>:8081` (Monitoring and management)

Note: Replace `<your-server-ip>` with your actual server IP address or domain name.

## 🔧 Proxy Features

This proxy server runs in **tunnel mode**, which provides certificate-free HTTPS proxying using HTTP CONNECT method. No SSL certificate installation is required on client devices.

## 🌐 Browser Configuration

Configure your browser to use the proxy:
- **Proxy Address**: `<your-server-ip>`
- **Proxy Port**: `8080`
- **Use for**: HTTP and HTTPS

## 🧪 Testing

Test the proxy connection:
```bash
# From your local machine
curl -x http://<your-server-ip>:8080 https://httpbin.org/ip

# Check proxy status from inside container
docker-compose exec tunnel-proxy curl -x http://localhost:8080 https://httpbin.org/ip
```

## 📊 Monitoring

Access the web interface at `http://<your-server-ip>:8081` to:
- View real-time request logs
- Monitor proxy performance
- Check proxy pool status
- Debug connection issues

You can also use Docker logs to monitor:
```bash
docker-compose logs -f tunnel-proxy
```

## 🛠️ Docker Commands

```bash
# Start the service
docker-compose up -d

# Stop the service
docker-compose down

# Restart the service
docker-compose restart

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose build --no-cache
docker-compose up -d
```

## ⚙️ Configuration

Customize behavior in `docker-compose.yml`:

```yaml
environment:
  - MITMPROXY_OPTS=--set confdir=/root/.mitmproxy
  - UPDATE_INTERVAL=300  # Proxy update interval (seconds)
  - TEST_BATCH_SIZE=10   # Proxies to test per batch
```

## 🐛 Troubleshooting

### Container Issues
```bash
# Check logs
docker-compose logs

# Rebuild image
docker-compose build --no-cache
```

### Port Conflicts
Modify ports in `docker-compose.yml`:
```yaml
ports:
  - "18080:8080"  # Change host port for proxy
  - "18081:8081"  # Change host port for web interface
```

### Certificate Issues
- Ensure certificate is properly installed in system
- Restart browser after certificate installation
- Check certificate trust settings

## 🚀 Production Deployment

For production environments:

```yaml
# docker-compose.yml
services:
  https-proxy:
    restart: always
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

MIT License

## 🤝 Contributing

Contributions are welcome! Please submit a Pull Request.

---

**Note**: This tool is for educational and testing purposes. Please ensure compliance with all applicable laws and terms of service when using proxy services.