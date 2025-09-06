#!/usr/bin/env python3
import requests
import sys
import warnings
warnings.filterwarnings('ignore')

def test_proxy_service():
    """测试代理服务"""
    proxy_url = "http://127.0.0.1:8080"
    
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    print("=" * 60)
    print("测试代理服务")
    print("=" * 60)
    print(f"\n代理地址: {proxy_url}")
    
    # 测试HTTPS网站
    test_urls = [
        "https://www.baidu.com",
        "https://httpbin.org/ip",
        "https://www.google.com"
    ]
    
    for url in test_urls:
        print(f"\n测试 {url}...")
        try:
            response = requests.get(
                url,
                proxies=proxies,
                timeout=10,
                verify=False  # 忽略SSL证书验证
            )
            
            print(f"  状态码: {response.status_code}")
            
            if "httpbin.org/ip" in url:
                print(f"  返回内容: {response.text[:200]}")
            else:
                print(f"  内容长度: {len(response.text)} 字节")
            
            print("  ✓ 测试成功")
            
        except requests.exceptions.ProxyError as e:
            print(f"  ❌ 代理错误: 请确保代理服务已启动在 {proxy_url}")
            print(f"     错误详情: {e}")
        except requests.exceptions.Timeout:
            print(f"  ❌ 请求超时")
        except Exception as e:
            print(f"  ❌ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_proxy_service()