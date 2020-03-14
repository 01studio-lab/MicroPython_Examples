# WiFi无线连接实验
#
# OpenMV通过WiFi拓展模块连接无线网络
#
# 翻译和注释：01Studio

import network

SSID='01Studio' # WiFi 账号
KEY='88888888'  # WiFi 密码

# 打印提示
print("Trying to connect... (may take a while)...")

#构建WiFi对象
wlan = network.WINC()

#连接网络
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)

#打印IP相关信息
print(wlan.ifconfig())
