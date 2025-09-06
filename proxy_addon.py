from mitmproxy import http, ctx
from proxy_manager import ProxyManager
import random

class ProxyAddon:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.failed_proxies = set()
        
    def request(self, flow: http.HTTPFlow) -> None:
        """处理每个请求，记录使用的代理信息"""
        # 获取一个可用的代理
        proxy = self.proxy_manager.get_random_proxy()
        
        if proxy:
            # 记录使用的代理（仅用于日志和追踪）
            flow.metadata["used_proxy"] = proxy
            ctx.log.info(f"标记使用代理: {proxy} 访问 {flow.request.pretty_host}")
        else:
            ctx.log.warn("没有可用的代理")
            flow.metadata["used_proxy"] = None
    
    def response(self, flow: http.HTTPFlow) -> None:
        """处理响应，记录代理状态"""
        if "used_proxy" in flow.metadata and flow.metadata["used_proxy"]:
            proxy = flow.metadata["used_proxy"]
            
            # 根据响应状态判断代理是否可用
            if flow.response and flow.response.status_code:
                if flow.response.status_code >= 500:
                    ctx.log.warn(f"代理 {proxy} 返回错误状态码: {flow.response.status_code}")
                    self.failed_proxies.add(proxy)
                elif flow.response.status_code == 200:
                    ctx.log.info(f"代理 {proxy} 工作正常")
                    # 从失败列表中移除
                    self.failed_proxies.discard(proxy)
    
    def error(self, flow: http.HTTPFlow) -> None:
        """处理错误，标记失败的代理"""
        if "used_proxy" in flow.metadata and flow.metadata["used_proxy"]:
            proxy = flow.metadata["used_proxy"]
            ctx.log.error(f"代理 {proxy} 连接失败")
            self.failed_proxies.add(proxy)

addons = [ProxyAddon()]