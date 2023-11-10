from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont
import subprocess
import os
import sys
import time 
from pathlib import Path
from datetime import datetime
import psutil

# Khởi tạo giao diện I2C
serial = i2c(port=1, address=0x3C)  # Thay đổi địa chỉ I2C nếu cần

# Khởi tạo thiết bị OLED SH1106
device = sh1106(serial, rotate=0)  # Thay đổi rotate nếu cần

# Tạo hình ảnh trống với chế độ 1-bit (đen và trắng)
image = Image.new("1", (device.width, device.height))

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return f"{n}B"
    
# Lấy đối tượng vẽ
draw = ImageDraw.Draw(image)
def get_ip_address(interface):
    cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface
    return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]
    
    
def get_cpu_usage():
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    return CPU


def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)

def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)

font = ImageFont.load_default()

while True:
    # Chọn font
    font = ImageFont.load_default()

    # Vẽ một dòng văn bản lên hình ảnh
    draw.text((0, 0), "IP:"+str(get_ip_address('eth0')), font=font, fill=255)
    draw.text((0, 10), mem_usage(), font=font, fill=255)

    # Figure out the width of the bar
    cmd = "free -m | awk 'NR==2{printf \"Mem:  %.0f%% %s/%s M\", $3*100/$2, $3,$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"GPU: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)

    draw.text((0, 20), str(MemUsage.decode('utf-8')), font=font, fill=255)
    draw.text((0, 30), str(Disk.decode('utf-8')), font=font, fill=255)
    draw.text((0, 40), str("Date: {}".format(datetime.datetime.now())), font=font, fill=255)
    # Hiển thị hình ảnh lên màn hình OLED
    device.display(image)
