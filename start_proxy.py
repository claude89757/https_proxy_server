#!/usr/bin/env python3
import subprocess
import sys
import os
import signal
import time

def check_port(port):
    """检查端口是否被占用"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def kill_process_on_port(port):
    """终止占用指定端口的进程"""
    try:
        result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"停止占用端口 {port} 的进程 (PID: {pid})")
                    subprocess.run(["kill", "-9", pid])
            time.sleep(1)
            return True
    except Exception as e:
        print(f"无法停止进程: {e}")
    return False

def main():
    """启动 mitmweb 代理服务"""
    print("=" * 60)
    print("启动 MITMWEB 代理服务")
    print("=" * 60)
    
    # 设置 mitmweb 参数
    port = 8080
    web_port = 8081
    
    # 检查端口是否被占用
    if check_port(port):
        print(f"端口 {port} 已被占用，正在清理...")
        if kill_process_on_port(port):
            print(f"已清理端口 {port}")
        else:
            print(f"无法清理端口 {port}，尝试使用其他端口")
            port = 8082
            print(f"改用端口 {port}")
    
    if check_port(web_port):
        print(f"Web端口 {web_port} 已被占用，正在清理...")
        if kill_process_on_port(web_port):
            print(f"已清理端口 {web_port}")
        else:
            print(f"无法清理端口 {web_port}，尝试使用其他端口")
            web_port = 8083
            print(f"改用端口 {web_port}")
    
    # 构建启动命令 - 使用完整路径
    mitmweb_path = "/Users/claude89757/Library/Python/3.9/bin/mitmweb"
    
    # 如果没有找到，尝试其他路径
    if not os.path.exists(mitmweb_path):
        # 尝试使用 which 命令查找
        try:
            result = subprocess.run(["which", "mitmweb"], capture_output=True, text=True)
            if result.returncode == 0:
                mitmweb_path = result.stdout.strip()
            else:
                mitmweb_path = "mitmweb"  # 回退到系统PATH
        except:
            mitmweb_path = "mitmweb"
    
    cmd = [
        mitmweb_path,
        "--listen-port", str(port),
        "--web-port", str(web_port),
        "--scripts", "proxy_addon.py",
        "--set", "confdir=~/.mitmproxy",
        "--ssl-insecure",  # 忽略上游服务器的SSL证书验证
        "--no-web-open-browser"  # 不自动打开浏览器
    ]
    
    print(f"\n配置信息:")
    print(f"  代理端口: {port}")
    print(f"  Web界面端口: {web_port}")
    print(f"  Web界面地址: http://127.0.0.1:{web_port}")
    print(f"\n代理配置:")
    print(f"  HTTP代理: http://127.0.0.1:{port}")
    print(f"  HTTPS代理: http://127.0.0.1:{port}")
    print("\n正在启动服务...")
    print("-" * 60)
    
    try:
        # 启动 mitmweb
        process = subprocess.Popen(cmd)
        
        print(f"\n✓ 服务已启动 (PID: {process.pid})")
        print("\n使用说明:")
        print("1. 在浏览器或应用中配置代理为 http://127.0.0.1:8080")
        print("2. 访问 http://127.0.0.1:8081 查看Web界面")
        print("3. 按 Ctrl+C 停止服务")
        print("\n代理池会自动每5分钟更新一次")
        print("-" * 60)
        
        # 等待进程结束
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n正在停止服务...")
        process.terminate()
        time.sleep(1)
        if process.poll() is None:
            process.kill()
        print("✓ 服务已停止")
    except FileNotFoundError:
        print("\n❌ 错误: 未找到 mitmweb 命令")
        print("请先安装 mitmproxy: pip install mitmproxy")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 检查依赖
    try:
        import mitmproxy
        import requests
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install mitmproxy requests")
        sys.exit(1)
    
    main()