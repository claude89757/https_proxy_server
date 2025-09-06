#!/usr/bin/env python3
"""
HTTP CONNECT 隧道代理服务器
无需客户端安装证书，支持透明的HTTPS代理
"""
import socket
import threading
import select
import time
import logging
from proxy_manager import ProxyManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TunnelProxy:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.proxy_manager = ProxyManager()
        self.stats = {
            'connections': 0,
            'bytes_transferred': 0,
            'active_connections': 0
        }
    
    def handle_connect_request(self, client_socket, request_line):
        """处理HTTP CONNECT请求"""
        try:
            # 解析CONNECT请求: CONNECT example.com:443 HTTP/1.1
            parts = request_line.split()
            if len(parts) < 2 or parts[0] != 'CONNECT':
                self.send_error_response(client_socket, "400 Bad Request")
                return False
            
            # 提取目标主机和端口
            target = parts[1]
            if ':' in target:
                host, port = target.split(':', 1)
                port = int(port)
            else:
                host = target
                port = 443  # 默认HTTPS端口
            
            logger.info(f"CONNECT请求: {host}:{port}")
            
            # 建立到目标服务器的连接
            target_socket = self.connect_to_target(host, port)
            if not target_socket:
                self.send_error_response(client_socket, "502 Bad Gateway")
                return False
            
            # 发送连接成功响应
            response = "HTTP/1.1 200 Connection Established\r\n\r\n"
            client_socket.send(response.encode())
            
            # 开始隧道转发
            self.start_tunnel(client_socket, target_socket, f"{host}:{port}")
            return True
            
        except Exception as e:
            logger.error(f"处理CONNECT请求失败: {e}")
            self.send_error_response(client_socket, "500 Internal Server Error")
            return False
    
    def connect_to_target(self, host, port):
        """连接到目标服务器，可选择通过上游代理"""
        # 尝试直接连接
        try:
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.settimeout(10)
            target_socket.connect((host, port))
            logger.info(f"直接连接到 {host}:{port} 成功")
            return target_socket
        except Exception as direct_error:
            logger.warning(f"直接连接 {host}:{port} 失败: {direct_error}")
        
        # 尝试通过上游代理连接
        proxy = self.proxy_manager.get_random_proxy()
        if proxy:
            try:
                proxy_parts = proxy.replace('http://', '').split(':')
                proxy_host = proxy_parts[0]
                proxy_port = int(proxy_parts[1])
                
                proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proxy_socket.settimeout(15)
                proxy_socket.connect((proxy_host, proxy_port))
                
                # 通过代理发送CONNECT请求
                connect_request = f"CONNECT {host}:{port} HTTP/1.1\r\n\r\n"
                proxy_socket.send(connect_request.encode())
                
                # 读取代理响应
                response = proxy_socket.recv(4096).decode()
                if "200 Connection Established" in response or "200 OK" in response:
                    logger.info(f"通过代理 {proxy} 连接到 {host}:{port} 成功")
                    return proxy_socket
                else:
                    logger.warning(f"代理 {proxy} 响应错误: {response[:100]}")
                    proxy_socket.close()
                    
            except Exception as proxy_error:
                logger.warning(f"代理连接 {proxy} 失败: {proxy_error}")
                if 'proxy_socket' in locals():
                    proxy_socket.close()
        
        return None
    
    def start_tunnel(self, client_socket, target_socket, target_info):
        """启动双向数据转发隧道"""
        self.stats['active_connections'] += 1
        
        def forward_data(source, destination, direction):
            """单向数据转发"""
            try:
                bytes_count = 0
                while True:
                    # 使用select进行非阻塞检查
                    ready, _, _ = select.select([source], [], [], 1.0)
                    if ready:
                        data = source.recv(4096)
                        if not data:
                            break
                        destination.send(data)
                        bytes_count += len(data)
                        self.stats['bytes_transferred'] += len(data)
                    else:
                        # 检查连接是否仍然活跃
                        try:
                            source.settimeout(0.1)
                            test_data = source.recv(1, socket.MSG_PEEK)
                            if not test_data:
                                break
                        except socket.timeout:
                            continue
                        except:
                            break
                        finally:
                            source.settimeout(None)
                            
            except Exception as e:
                logger.debug(f"数据转发结束 {direction}: {e}")
            finally:
                logger.info(f"隧道关闭 {target_info} - {direction}: 传输 {bytes_count} 字节")
        
        # 创建双向转发线程
        client_to_target = threading.Thread(
            target=forward_data,
            args=(client_socket, target_socket, f"客户端->目标"),
            daemon=True
        )
        target_to_client = threading.Thread(
            target=forward_data,
            args=(target_socket, client_socket, f"目标->客户端"),
            daemon=True
        )
        
        client_to_target.start()
        target_to_client.start()
        
        # 等待任一方向的连接关闭
        client_to_target.join()
        target_to_client.join()
        
        # 清理连接
        try:
            client_socket.close()
        except:
            pass
        try:
            target_socket.close()
        except:
            pass
            
        self.stats['active_connections'] -= 1
    
    def send_error_response(self, client_socket, error):
        """发送HTTP错误响应"""
        try:
            response = f"HTTP/1.1 {error}\r\nConnection: close\r\n\r\n"
            client_socket.send(response.encode())
        except:
            pass
    
    def handle_client(self, client_socket, client_address):
        """处理客户端连接"""
        try:
            self.stats['connections'] += 1
            logger.info(f"新连接来自: {client_address}")
            
            # 读取客户端请求
            client_socket.settimeout(30)  # 30秒超时
            request_data = b""
            
            while b"\r\n\r\n" not in request_data:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                request_data += chunk
                if len(request_data) > 8192:  # 限制请求大小
                    break
            
            if not request_data:
                logger.warning(f"客户端 {client_address} 未发送数据")
                return
            
            request_text = request_data.decode('utf-8', errors='ignore')
            request_lines = request_text.split('\r\n')
            request_line = request_lines[0]
            
            # 处理CONNECT请求
            if request_line.startswith('CONNECT'):
                self.handle_connect_request(client_socket, request_line)
            else:
                # 不支持的请求类型
                logger.warning(f"不支持的请求: {request_line}")
                self.send_error_response(client_socket, "405 Method Not Allowed")
                
        except socket.timeout:
            logger.warning(f"客户端 {client_address} 超时")
        except Exception as e:
            logger.error(f"处理客户端 {client_address} 时发生错误: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def start_stats_logger(self):
        """启动状态日志线程"""
        def log_stats():
            while True:
                time.sleep(60)  # 每分钟记录一次
                logger.info(
                    f"状态 - 总连接: {self.stats['connections']}, "
                    f"活跃连接: {self.stats['active_connections']}, "
                    f"传输字节: {self.stats['bytes_transferred']}"
                )
        
        stats_thread = threading.Thread(target=log_stats, daemon=True)
        stats_thread.start()
    
    def start(self):
        """启动代理服务器"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(128)
            
            logger.info(f"🚀 HTTP CONNECT隧道代理服务器启动")
            logger.info(f"📍 监听地址: {self.host}:{self.port}")
            logger.info(f"🔧 配置代理: http://{self.host}:{self.port}")
            logger.info(f"✅ 无需安装证书，支持所有HTTPS网站")
            logger.info("=" * 50)
            
            # 启动状态日志
            self.start_stats_logger()
            
            while True:
                client_socket, client_address = server_socket.accept()
                
                # 为每个客户端创建处理线程
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            logger.info("\n🛑 收到停止信号，正在关闭服务器...")
        except Exception as e:
            logger.error(f"❌ 服务器错误: {e}")
        finally:
            server_socket.close()
            logger.info("✅ 服务器已关闭")

def main():
    """主函数"""
    import sys
    
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error("无效端口号")
            sys.exit(1)
    
    proxy = TunnelProxy(port=port)
    proxy.start()

if __name__ == "__main__":
    main()