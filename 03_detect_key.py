# -*- coding: utf-8 -*
import RPi.GPIO as GPIO
import time
import Tkinter as tk
import threading

GPIO.setmode(GPIO.BCM)
# 定义 GPIO 引脚
SCLK = 16
RCLK = 20
DIO = 21

KEY1 = 13
KEY2 = 19
KEY3 = 26

# 全局变量
value = 10
red_value = 1
yellow_value = 1
green_value = 1

# 定义字模
LED_Library = [0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8, 0x80, 0x90, 0x8C,
               0xBF, 0xC6, 0xA1, 0x86, 0x8E, 0xbf]

LED_PINS = [SCLK, RCLK, DIO]
for led_pin in LED_PINS:
    GPIO.setup(led_pin, GPIO.OUT)  # 设置 GPIO 引脚为输出

GPIO.setup(KEY1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(KEY2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(KEY3, GPIO.IN, GPIO.PUD_UP)


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


def setTkValue():
    global value, value_str, value1, red_str, red_value, yellow_str, yellow_value, green_str, green_value
    value_str.set("%s" % value)
    red_str.set("%s" % red_value)
    yellow_str.set("%s" % yellow_value)
    green_str.set("%s" % green_value)


def key_callback(channel):  # 定义中断响应函数
    global value, value_str, value1, red_str, red_value, yellow_str, yellow_value, green_str, green_value
    if(channel == 13 and value > 0):  # 接红色键
        value = value-1
        red_value = 0
        yellow_value = 1
        green_value = 1
        setTkValue()

    if(channel == 19):  # 接黄色键
        value = 0
        red_value = 1
        yellow_value = 0
        green_value = 1
        setTkValue()

    if(channel == 26 and value < 9999):  # 接绿色键
        value = value+1
        red_value = 1
        yellow_value = 1
        green_value = 0
        setTkValue()


def initialTk():
    global value, value_str, value1, red_str, red_value, yellow_str, yellow_value, green_str, green_value, window
    # 显示value动态变化值
    value_str = tk.StringVar()
    value_str.set("%s" % value)
    label1 = tk.Label(window, text="value:", fg='black',
                      font=('宋体', 35))  # 用于显示警告信息
    value1 = tk.Label(window, textvariable=value_str,
                      fg='black', font=('宋体', 35))  # 用于显示警告信息
    label1.place(x=20, y=20, anchor='nw')
    value1.place(x=280, y=20, anchor='nw')

    # 显示红色按键动态变化值
    red_str = tk.StringVar()
    red_str.set("%s" % red_value)
    red_label = tk.Label(window, text="red key:", fg='black', font=('宋体', 35))
    red_value = tk.Label(window, textvariable=red_str,
                         fg='black', font=('宋体', 35))
    red_label.place(x=20, y=80, anchor='nw')
    red_value.place(x=280, y=80, anchor='nw')

    # 显示黄色按键动态变化值
    yellow_str = tk.StringVar()
    yellow_str.set("%s" % yellow_value)
    yellow_label = tk.Label(window, text="yellow key:",
                            fg='black', font=('宋体', 35))  # 用于显示警告信息
    yellow_value = tk.Label(window, textvariable=yellow_str,
                            fg='black', font=('宋体', 35))  # 用于显示警告信息
    yellow_label.place(x=20, y=140, anchor='nw')
    yellow_value.place(x=280, y=140, anchor='nw')

    # 显示绿色按键动态变化值
    green_str = tk.StringVar()
    green_str.set("%s" % green_value)
    green_label = tk.Label(window, text="green key:",
                           fg='black', font=('宋体', 35))  # 用于显示警告信息
    green_value = tk.Label(window, textvariable=green_str,
                           fg='black', font=('宋体', 35))
    green_label.place(x=20, y=200, anchor='nw')
    green_value.place(x=280, y=200, anchor='nw')


def tK_Show():
    global value, value_str, value1, red_str, red_value, yellow_str, yellow_value, green_str, green_value, window
    window = tk.Tk()  # 第1步，实例化object，建立窗口window
    window.title('window_3')  # 第2步，给窗口的可视化起名字
    window.geometry('1000x600')  # 第3步，设定窗口的大小(长 * 宽)
    initialTk()
    window.mainloop()


def LED_Show():
    while True:
        Show(value)


# 注册中断事件
GPIO.add_event_detect(KEY1, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(KEY2, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(KEY3, GPIO.FALLING, bouncetime=200)
# 绑定中断响应函数
GPIO.add_event_callback(KEY1, callback=key_callback)
GPIO.add_event_callback(KEY2, callback=key_callback)
GPIO.add_event_callback(KEY3, callback=key_callback)

if __name__ == '__main__':
    # 用于在数码管上显示值
    thread1 = threading.Thread(target=LED_Show, args=())
    # 用于创建TK窗口，并显示对应的值
    thread2 = threading.Thread(target=tK_Show, args=())
    
    thread1.start()  # thread1执行
    thread2.start()  # thread2执行
    # 等待线程结束
    thread1.join()
    thread2.join()

    GPIO.cleanup()
