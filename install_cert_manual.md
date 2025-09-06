# 手动安装 mitmproxy 证书指南 (macOS)

## 步骤 1: 打开证书文件
```bash
open ~/.mitmproxy/
```
找到 `mitmproxy-ca-cert.pem` 文件，双击打开

## 步骤 2: 添加到钥匙串
1. 系统会弹出"添加证书"对话框
2. 选择"系统"钥匙串
3. 点击"添加"
4. 输入系统密码

## 步骤 3: 信任证书（重要！）
```bash
# 打开钥匙串访问
open /Applications/Utilities/Keychain\ Access.app
```

1. 在左侧选择"系统"
2. 搜索 "mitmproxy"
3. 双击 mitmproxy 证书
4. 展开"信任"部分
5. 将"使用此证书时"改为"始终信任"
6. 关闭窗口，输入密码确认

## 步骤 4: 重启 Chrome
完全关闭 Chrome 后重新打开

## 验证
访问 https://www.baidu.com，不应该再有证书警告