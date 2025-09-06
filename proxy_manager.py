import requests
import threading
import time
from datetime import datetime
import random
import warnings
warnings.filterwarnings('ignore')

class ProxyManager:
    def __init__(self):
        self.proxy_list_url = "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/isz_https_proxies.txt"
        self.available_proxies = []
        self.all_proxies = []
        self.lock = threading.Lock()
        self.update_interval = 300  # 5分钟更新一次
        self.test_batch_size = 10  # 每批测试10个代理
        self.start_update_thread()
    
    def fetch_proxies_from_github(self):
        """从 GitHub 获取代理列表"""
        try:
            response = requests.get(self.proxy_list_url, timeout=10)
            if response.status_code == 200:
                proxies = []
                for line in response.text.strip().split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        proxies.append(line)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 从 GitHub 获取到 {len(proxies)} 个代理")
                return proxies
        except Exception as e:
            print(f"获取代理列表失败: {e}")
        return []
    
    def check_proxy(self, proxy_url):
        """使用 requests 检查代理是否可用"""
        try:
            target_url = 'https://ftty.ydmap.cn/srv100241/api/pub/sport/venue/getVenueOrderList?salesItemId=100341&curDate=1748188800000&venueGroupId=&t=1748187760876&type__1295=n4%2BxnDR70%3DK7wqWqY5DsD7fmKD54sO2g8S4rTD'
            
            headers = {
                'Host': 'ftty.ydmap.cn',
                'server-reflexive-ip': '1.1.1.1',
                'entry-tag': '',
                'access-token': '',
                'visitor-id': 'xxxxxx',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000) MacWechat/3.8.10(0x13080a10) XWEB/1227 Flue',
                'accept': 'application/json, text/plain, */*',
                'timestamp': '1748187760918',
                'signature': 'xxxxxx',
                'tab-id': 'ydmap_fb21e370a0f048acfef6a518e9952c02',
                'x-requested-with': 'XMLHttpRequest',
                'cross-token': '',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://ftty.ydmap.cn/booking/schedule/101332?salesItemId=100341',
                'accept-language': 'zh-CN,zh;q=0.9'
            }
            
            proxies = {
                'http': f'http://{proxy_url}',
                'https': f'http://{proxy_url}'
            }
            
            response = requests.get(
                target_url,
                headers=headers,
                proxies=proxies,
                timeout=3,
                verify=False
            )
            
            response_text = response.text
            
            # 判断返回内容是否包含"签名"，表示代理IP可用
            if "签名" in response_text or "验证" in response_text:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{now}] 发现可用代理: {proxy_url}")
                return True
                
        except Exception as e:
            pass
        return False
    
    def test_proxies(self, proxy_list):
        """批量测试代理"""
        available = []
        for proxy in proxy_list:
            if self.check_proxy(proxy):
                available.append(proxy)
        return available
    
    def update_proxies(self):
        """更新代理池"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始更新代理池...")
        
        # 获取新的代理列表
        new_proxies = self.fetch_proxies_from_github()
        if not new_proxies:
            print("未获取到新代理，保持现有代理池")
            return
        
        # 随机选择一批代理进行测试
        test_sample = random.sample(new_proxies, min(self.test_batch_size, len(new_proxies)))
        available = self.test_proxies(test_sample)
        
        # 同时测试现有的可用代理
        if self.available_proxies:
            print(f"重新测试现有 {len(self.available_proxies)} 个可用代理...")
            still_available = self.test_proxies(self.available_proxies)
            available.extend(still_available)
        
        # 更新代理池
        with self.lock:
            self.all_proxies = new_proxies
            self.available_proxies = list(set(available))
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 代理池更新完成，可用代理数: {len(self.available_proxies)}")
    
    def update_thread(self):
        """定期更新代理的线程"""
        while True:
            try:
                self.update_proxies()
            except Exception as e:
                print(f"更新代理池出错: {e}")
            time.sleep(self.update_interval)
    
    def start_update_thread(self):
        """启动更新线程"""
        thread = threading.Thread(target=self.update_thread, daemon=True)
        thread.start()
        # 立即执行一次更新
        self.update_proxies()
    
    def get_random_proxy(self):
        """获取一个随机的可用代理"""
        with self.lock:
            if self.available_proxies:
                return random.choice(self.available_proxies)
            elif self.all_proxies:
                # 如果没有测试过的可用代理，随机返回一个未测试的
                return random.choice(self.all_proxies)
        return None
    
    def get_all_available_proxies(self):
        """获取所有可用代理"""
        with self.lock:
            return self.available_proxies.copy()