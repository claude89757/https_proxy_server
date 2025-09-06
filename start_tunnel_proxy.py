#!/usr/bin/env python3
"""
启动HTTP CONNECT隧道代理服务器
无需证书安装的HTTPS代理解决方案
"""
import subprocess
import sys
import os
import signal
import time
import argparse

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
    """启动隧道代理服务器"""
    parser = argparse.ArgumentParser(description='HTTP CONNECT隧道代理服务器')
    parser.add_argument('--port', '-p', type=int, default=10800, help='代理服务端口 (默认: 10800)')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='监听地址 (默认: 0.0.0.0)')
    parser.add_argument('--force', '-f', action='store_true', help='强制清理端口冲突')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 HTTP CONNECT 隧道代理服务器")
    print("=" * 60)
    print("✅ 特性:")
    print("  • 无需安装SSL证书")
    print("  • 支持所有HTTPS网站")
    print("  • 透明的端到端加密")
    print("  • 自动代理池管理")
    print()
    
    # 检查端口是否被占用
    if check_port(args.port):
        if args.force or input(f"端口 {args.port} 已被占用，是否清理? (y/N): ").lower() == 'y':
            if kill_process_on_port(args.port):
                print(f"✅ 已清理端口 {args.port}")
            else:
                print(f"❌ 无法清理端口 {args.port}")
                sys.exit(1)
        else:
            print("❌ 端口被占用，启动失败")
            sys.exit(1)
    
    print(f"📍 配置信息:")
    print(f"  监听地址: {args.host}:{args.port}")
    print(f"  代理配置: http://{args.host}:{args.port}")
    
    if args.host == '0.0.0.0':
        print(f"\n⚠️  安全提醒:")
        print(f"  服务监听所有网络接口，请确保:")
        print(f"  • 使用防火墙限制访问")
        print(f"  • 在受信任的网络环境中部署")
    
    print(f"\n🔧 客户端配置:")
    print(f"  HTTP代理: http://<服务器IP>:{args.port}")
    print(f"  HTTPS代理: http://<服务器IP>:{args.port}")
    print(f"  (无需安装证书)")
    
    print("\n" + "=" * 60)
    print("正在启动服务...")
    
    try:
        # 检查依赖
        try:
            from tunnel_proxy import TunnelProxy
            from proxy_manager import ProxyManager
        except ImportError as e:
            print(f"❌ 导入模块失败: {e}")
            print("请确保所有依赖文件都在当前目录")
            sys.exit(1)
        
        # 启动隧道代理服务器
        proxy = TunnelProxy(host=args.host, port=args.port)
        proxy.start()
        
    except KeyboardInterrupt:
        print("\n\n🛑 收到停止信号...")
        print("✅ 服务已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()