# HTTPS Proxy Server

A robust HTTPS proxy server built with mitmproxy that automatically maintains a pool of working proxies from GitHub sources.

## 🚀 Features

- **Automatic Proxy Pool Management**: Fetches and updates proxy list from GitHub every 5 minutes
- **Health Check System**: Continuously validates proxy availability against target websites
- **Real-time Monitoring**: Web interface to monitor proxy requests and traffic
- **SSL/TLS Support**: Full HTTPS interception with certificate management
- **Chrome Integration**: Easy browser setup with dedicated launch script
- **Thread-safe Operations**: Concurrent proxy testing and management

## 📁 Project Structure

```
https_proxy_server/
├── proxy_manager.py      # Core proxy pool manager (fetching, testing, maintenance)
├── proxy_addon.py        # mitmproxy addon for request handling and monitoring
├── start_proxy.py        # Main application launcher
├── test_proxy.py         # Proxy testing utility
├── start_chrome_proxy.sh # Chrome browser launcher with proxy settings
├── install_cert_manual.md # SSL certificate installation guide
└── requirements.txt      # Python dependencies
```

## 🔧 Installation

### Prerequisites
- Python 3.7+
- pip3

### Setup

1. Clone the repository:
```bash
git clone https://github.com/claude89757/https_proxy_server.git
cd https_proxy_server
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## 📖 Usage

### 1. SSL Certificate Setup (First Time Only)

For HTTPS traffic interception, you need to install the mitmproxy certificate:
- Follow the instructions in `install_cert_manual.md`
- The certificate ensures secure HTTPS proxy functionality

### 2. Start the Proxy Server

```bash
python3 start_proxy.py
```

This will start:
- **Proxy server**: `http://127.0.0.1:8080`
- **Web monitoring interface**: `http://127.0.0.1:8081`

### 3. Configure Your Browser

#### Option A: Use Dedicated Chrome Instance (Recommended)
```bash
./start_chrome_proxy.sh
```
This launches Chrome with pre-configured proxy settings.

#### Option B: Manual System Proxy Configuration
1. Go to System Settings → Network → Advanced → Proxies
2. Set HTTP/HTTPS proxy to: `127.0.0.1:8080`

### 4. Test the Proxy

Verify the proxy is working:
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

The proxy manager includes configurable parameters:
- Update interval: 5 minutes (default)
- Test batch size: 10 proxies per batch
- Timeout settings for proxy validation
- Target URL for health checks

## 🛡️ Security Notes

- The proxy server requires SSL certificate installation for HTTPS interception
- All traffic passes through the local mitmproxy instance
- Proxy credentials and sensitive data are handled securely
- Regular proxy rotation enhances anonymity

## 📊 Monitoring

Access the web interface at `http://127.0.0.1:8081` to:
- View real-time request logs
- Monitor proxy performance
- Check proxy pool status
- Debug connection issues

## 🐛 Troubleshooting

### Port Already in Use
The application automatically handles port conflicts by:
- Detecting and terminating existing processes
- Using alternative ports if needed

### Certificate Issues
- Ensure the mitmproxy certificate is properly installed in your system keychain
- For Chrome: Check that certificates are trusted for SSL

### No Available Proxies
- The system will continuously retry fetching proxies from GitHub
- Check your internet connection
- Verify the GitHub source URL is accessible

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Note**: This tool is for educational and testing purposes. Please ensure compliance with all applicable laws and terms of service when using proxy services.