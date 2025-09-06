#!/usr/bin/env python3
"""
测试HTTP CONNECT隧道代理功能
"""
import requests
import subprocess
import time
import threading
import sys
import socket

def test_proxy_connection(proxy_url, test_urls):
    """测试代理连接"""
    print(f"🔄 测试代理: {proxy_url}")
    
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    results = []
    
    for url in test_urls:
        try:
            print(f"  测试 {url}...")
            response = requests.get(url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                print(f"  ✅ {url} - 状态码: {response.status_code}")
                results.append(True)
            else:
                print(f"  ⚠️  {url} - 状态码: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"  ❌ {url} - 错误: {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"📊 成功率: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    return success_rate

def test_direct_connection(test_urls):
    """测试直接连接作为对照"""
    print("🌐 测试直接连接 (不使用代理)")
    
    results = []
    for url in test_urls:
        try:
            print(f"  测试 {url}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"  ✅ {url} - 状态码: {response.status_code}")
                results.append(True)
            else:
                print(f"  ⚠️  {url} - 状态码: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"  ❌ {url} - 错误: {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"📊 直连成功率: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    return success_rate

def check_proxy_server(host='127.0.0.1', port=8080):
    """检查代理服务器是否运行"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 HTTP CONNECT 隧道代理测试")
    print("=" * 60)
    
    # 测试URL列表
    test_urls = [
        'https://httpbin.org/ip',
        'https://www.google.com',
        'https://www.github.com',
        'https://httpbin.org/get',
        'https://jsonplaceholder.typicode.com/posts/1'
    ]
    
    proxy_host = '127.0.0.1'
    proxy_port = 10800
    proxy_url = f'http://{proxy_host}:{proxy_port}'
    
    print(f"🎯 测试目标:")
    for i, url in enumerate(test_urls, 1):
        print(f"  {i}. {url}")
    print()
    
    # 检查代理服务器是否运行
    if not check_proxy_server(proxy_host, proxy_port):
        print(f"❌ 代理服务器 {proxy_url} 未运行")
        print(f"请先启动代理服务器: python start_tunnel_proxy.py")
        
        # 询问是否启动代理服务器
        if input("是否自动启动代理服务器? (y/N): ").lower() == 'y':
            print("🚀 启动代理服务器...")
            try:
                # 在后台启动代理服务器
                proxy_process = subprocess.Popen([
                    sys.executable, 'start_tunnel_proxy.py', '--port', str(proxy_port)
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # 等待服务器启动
                for i in range(10):
                    time.sleep(1)
                    if check_proxy_server(proxy_host, proxy_port):
                        print("✅ 代理服务器已启动")
                        break
                    print(f"  等待启动... ({i+1}/10)")
                else:
                    print("❌ 代理服务器启动失败")
                    return
                
                try:
                    # 运行测试
                    run_tests(proxy_url, test_urls)
                finally:
                    # 停止代理服务器
                    print("\n🛑 停止代理服务器...")
                    proxy_process.terminate()
                    proxy_process.wait()
                    
            except Exception as e:
                print(f"❌ 启动代理服务器失败: {e}")
                return
        else:
            return
    else:
        print(f"✅ 代理服务器 {proxy_url} 正在运行")
        run_tests(proxy_url, test_urls)

def run_tests(proxy_url, test_urls):
    """运行所有测试"""
    print("\n" + "="*60)
    
    # 测试直连
    direct_success = test_direct_connection(test_urls)
    
    print("\n" + "="*60)
    
    # 测试代理连接
    proxy_success = test_proxy_connection(proxy_url, test_urls)
    
    print("\n" + "="*60)
    print("📋 测试总结:")
    print(f"  直连成功率: {direct_success:.1f}%")
    print(f"  代理成功率: {proxy_success:.1f}%")
    
    if proxy_success >= 80:
        print("🎉 代理功能正常！")
    elif proxy_success >= 50:
        print("⚠️  代理部分正常，建议检查网络或代理池")
    else:
        print("❌ 代理功能异常，需要检查配置")
    
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 测试被中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")