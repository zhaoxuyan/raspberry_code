# 连接设备需要
# hcitool scan
# sudo rfcomm connect 0 98:D3:11:FC:1F:BA

import RPi.GPIO as GPIO
import serial 
import time 
import threading 

# 采用BCM编码方式
GPIO.setmode(GPIO.BCM) 

# 将L0~L7对应的引脚
LED_PINS = [18, 23, 24, 25, 12, 16, 20, 21]

for led_pin in LED_PINS:
    # 输出
    GPIO.setup(led_pin, GPIO.OUT)
    # 初始化让所有灯熄灭
    GPIO.output(led_pin, GPIO.HIGH)

# 树莓派连接串行口
ser1 = serial.Serial('/dev/rfcomm0', 9600) 
# 使用USB连接串行口
ser2 = serial.Serial("/dev/ttyUSB0", 9600)

# 显示对应的LED灯
def Led_Show(data):
    for index, value in enumerate(data):
        if value == 0:
            GPIO.output(LED_PINS[index], GPIO.LOW)
        elif value == 1:
            GPIO.output(LED_PINS[index], GPIO.HIGH)

# 板载蓝牙接收信息
def rasp_recieve():
    while True:
        recv = None
        count = ser1.inWaiting() # inWaiting 返回接收缓存中的字节数
        if count != 0:
            recv = str(ser1.read(count), encoding="utf-8")
            data = [int(i) for i in list(recv)]
            Led_Show(data)
        time.sleep(2)

# HC-05蓝牙模块发送信息
def hc_send():
    while True:
        message = input(" 请输入八个数字控制LED灯(只包含0和1): ")
        for i in message: 
            if i != "0" and i != "1":
                print ("Illegal input!")
                break
        ser2.write(message.encode())
        time.sleep(3)

thread1 = threading.Thread(target=rasp_recieve, args=())
thread2 = threading.Thread(target=hc_send, args=())
thread1.start() # thread1执行
thread2.start() # thread2执行
thread1.join() 
thread2.join()