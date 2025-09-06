#!/bin/bash

echo "启动 Chrome with Proxy..."

# 关闭现有 Chrome 进程
pkill -f "Google Chrome"
sleep 1

# 启动 Chrome 并配置代理
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --proxy-server="http://127.0.0.1:8080" \
  --user-data-dir="/tmp/chrome-proxy-profile" \
  &

echo "Chrome 已启动，使用代理: http://127.0.0.1:8080"
echo "访问 http://127.0.0.1:8081 查看 mitmweb 界面"