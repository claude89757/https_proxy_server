# MITMWEB 代理服务

使用 mitmproxy 搭建的代理服务，自动从 GitHub 获取并维护可用代理池。

## 功能特点

- 自动从 GitHub 获取代理列表（每5分钟更新）
- 自动测试代理可用性（针对特定目标网站）
- 自动剔除不可用代理
- 代理池管理和状态监控
- Web界面实时查看请求

## 文件说明

```
proxy/
├── proxy_manager.py      # 代理管理器（获取、测试、维护代理池）
├── proxy_addon.py        # mitmproxy 插件（记录代理使用情况）
├── start_proxy.py        # 启动脚本
├── test_proxy.py         # 测试脚本
├── start_chrome_proxy.sh # Chrome代理启动脚本
├── install_cert_manual.md # 证书安装指南
└── requirements.txt      # 依赖包
```

## 安装

```bash
# 安装依赖
pip3 install mitmproxy requests

# 或使用 requirements.txt
pip3 install -r requirements.txt
```

## 使用方法

### 1. 配置证书（首次使用）

参考 `install_cert_manual.md` 手动安装证书到系统钥匙串。

### 2. 启动代理服务

```bash
python3 start_proxy.py
```

服务启动后：
- 代理端口：http://127.0.0.1:8080
- Web监控界面：http://127.0.0.1:8081

### 3. 配置浏览器

**方法A：使用专用Chrome实例（推荐）**
```bash
./start_chrome_proxy.sh
```

**方法B：系统代理设置**
- 系统设置 > 网络 > 高级 > 代理
- HTTP/HTTPS代理：127.0.0.1:8080

### 4. 测试代理

```bash
python3 test_proxy.py
```

## 工作原理

1. `proxy_manager.py` 定期从 GitHub 获取代理列表
2. 使用提供的测试函数验证代理可用性
3. mitmproxy 作为本地代理服务器运行
4. `proxy_addon.py` 记录和监控代理使用情况

## 注意事项

- 代理池每5分钟自动更新
- 仅保留通过特定网站测试的可用代理
- 证书必须正确安装才能代理HTTPS流量
- 端口冲突时会自动清理或使用备用端口# https_proxy_server
