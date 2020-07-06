# -*- coding: utf-8 -*
import RPi.GPIO as GPIO
import time
import Tkinter as tk
import threading

# 全局变量
value = 0

GPIO.setmode(GPIO.BCM)
# 定义 GPIO 引脚
SCLK = 16
RCLK = 20
DIO = 21


# 定义字模
LED_Library = [0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8, 0x80, 0x90, 0x8C, 0xBF, 0xC6, 0xA1, 0x86, 0x8E, 0xbf]

LED_PINS = [SCLK, RCLK, DIO]
for led_pin in LED_PINS:
    GPIO.setup(led_pin, GPIO.OUT)  # 设置 GPIO 引脚为输出

# 超声波模块
GPIO_TRIGGER = 13
GPIO_ECHO = 19
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def Show(i_data):
    while i_data > 10000:  # 限制数据大小
        i_data = i_data-10000
    if(i_data >= 1000):
        i_show1 = i_data//1000
        i_data -= 1000*i_show1
    else:
        i_show1 = 0
    if(i_data >= 100):
        i_show2 = i_data//100
        i_data -= 100*i_show2
    else:
        i_show2 = 0
    if(i_data >= 10):
        i_show3 = i_data//10
        i_data -= 10*i_show3
    else:
        i_show3 = 0
    i_show4 = i_data
    LED4_Display(i_show1, 0x08)
    LED4_Display(i_show2, 0x04)
    LED4_Display(i_show3, 0x02)
    LED4_Display(i_show4, 0x01)

def LED4_Display(i_index, hx_location):
    LED_OUT(LED_Library[i_index])  # 输出字模
    LED_OUT(hx_location)  # 输出位置
    GPIO.output(RCLK, GPIO.LOW)  # 在 RCLK 输出向上脉冲
    GPIO.output(RCLK, GPIO.HIGH)

def LED_OUT(X):
    for i in range(0, 8):
        if(X & 0x80):
            GPIO.output(DIO, GPIO.HIGH)
        else:
            GPIO.output(DIO, GPIO.LOW)
        GPIO.output(SCLK, GPIO.LOW)  # 在 SCLK 输出向上脉冲
        GPIO.output(SCLK, GPIO.HIGH)
        X <<= 1

def led_show():
    while True:
        Show(value)

def distance():
    global value
    # 发送高电平信号到 Trig 引脚
    GPIO.output(GPIO_TRIGGER, True)
 
    # 持续 10 us 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    start_time = time.time()
    stop_time = time.time()
 
    # 记录发送超声波的时刻1
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
 
    # 记录接收到返回超声波的时刻2
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
 
    # 计算超声波的往返时间 = 时刻2 - 时刻1
    time_elapsed = stop_time - start_time
    # 声波的速度为 343m/s， 转化为 34300cm/s。
    distance = (time_elapsed * 34300) / 2
    value = int(distance)
    time.sleep(0.5)
    print value

def get_distance():
    while True:
        distance()

if __name__ == '__main__':
    # 用于在数码管上显示值
    thread1 = threading.Thread(target=led_show, args=())
    # 用于获取超声波测距结果
    thread2 = threading.Thread(target=get_distance, args=())
    
    thread1.start()  # thread1执行
    thread2.start()  # thread2执行
    # 等待线程结束
    thread1.join()
    thread2.join()

    GPIO.cleanup()