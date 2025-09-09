# HTTPS Proxy Server

HTTP CONNECT tunnel proxy with automatic proxy pool management from GitHub sources.

## 🔧 Quick Start

### Docker (Recommended)

```bash
# Clone and start
git clone https://github.com/claude89757/https_proxy_server.git
cd https_proxy_server
docker-compose up -d
```

### Python Direct

```bash
# Clone and install
git clone https://github.com/claude89757/https_proxy_server.git
cd https_proxy_server
pip install -r requirements.txt

# Start proxy server
python start_tunnel_proxy.py --host 0.0.0.0 --port 8080
```

- **Proxy**: `http://<your-server-ip>:8080`
- **Web UI**: `http://<your-server-ip>:8081`

## Testing

```bash
curl -x http://<your-server-ip>:8080 https://httpbin.org/ip
```