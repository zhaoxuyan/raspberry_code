# -*- coding: utf-8 -*
import Tkinter as tk
import threading
import RPi.GPIO as GPIO
import time
#IIC 库
import smbus

# 全局变量
window = None
show_value = -1
light_value = -2
heat_value = -3
show_value_str = None
light_value_str = None
heat_value_str = None

bcm_list1 = [16, 20, 21]
bcm_list2 = [13, 19, 26]

class Show(threading.Thread):
    def __init__(self, threadID, bcm_list, control_num):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.SCLK = bcm_list[0]
        self.RCLK = bcm_list[1]
        self.DIO = bcm_list[2]
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        # 设置 GPIO 引脚为输出
        LED_PINS = [self.SCLK, self.RCLK, self.DIO]
        for led_pin in LED_PINS:
            self.GPIO.setup(led_pin, self.GPIO.OUT)
        # 选择控制哪个电阻
        self.control_num = control_num
        # 定义字模
        self.LED_Library = [0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8, 0x80, 0x90, 0x8C, 0xBF, 0xC6, 0xA1, 0x86, 0x8E, 0xbf]

    def run(self):
        global show_value, light_value
        print("Starting " + self.name)
        
        # digital tube
        while True:
            # 可变电阻
            if self.control_num == 0:
                time.sleep(0.00001)
                self.led_show(show_value)
            # 光敏电阻
            elif self.control_num == 2:
                time.sleep(0.00001)
                self.led_show(light_value)
        
        
    def led_show(self, i_data):
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
        self.LED4_Display(i_show1, 0x08)
        self.LED4_Display(i_show2, 0x04)
        self.LED4_Display(i_show3, 0x02)
        self.LED4_Display(i_show4, 0x01)

    def LED4_Display(self, i_index, hx_location):
        self.LED_OUT(self.LED_Library[i_index])  # 输出字模
        self.LED_OUT(hx_location)  # 输出位置
        self.GPIO.output(self.RCLK, self.GPIO.LOW)  # 在 RCLK 输出向上脉冲
        self.GPIO.output(self.RCLK, self.GPIO.HIGH)

    def LED_OUT(self, X):
        for i in range(0, 8):
            if(X & 0x80):
                self.GPIO.output(self.DIO, self.GPIO.HIGH)
            else:
                self.GPIO.output(self.DIO, self.GPIO.LOW)
            self.GPIO.output(self.SCLK, self.GPIO.LOW)  # 在 SCLK 输出向上脉冲
            self.GPIO.output(self.SCLK, self.GPIO.HIGH)
            X <<= 1

    
class TK(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        
    def run(self):
        global show_value, light_value, show_value_str, light_value_str, window
        print("Starting " + self.name)
        self.tK_Show()
        
    def tK_Show(self):
        global show_value, light_value, show_value_str, light_value_str, window
        window = tk.Tk()  # 第1步，实例化object，建立窗口window
        window.title('window_tk_1')  # 第2步，给窗口的可视化起名字
        window.geometry('1000x600')  # 第3步，设定窗口的大小(长 * 宽)
        self.initialTk()
        window.mainloop()
        
    def initialTk(self):
        global show_value, light_value, heat_value, show_value_str, light_value_str, heat_value_str, window
        # 显示可变电阻 动态变化值
        show_value_str = tk.StringVar()
        show_value_str.set("%s" % show_value)
        label1 = tk.Label(window, text="可变电阻:", fg='black', font=('宋体', 30))
        value1 = tk.Label(window, textvariable=show_value_str, fg='black', font=('宋体', 35))  # 用于显示警告信息
        label1.place(x=20, y=20, anchor='nw')
        value1.place(x=200, y=20, anchor='nw')

        # 显示光敏电阻 动态变化值
        light_value_str = tk.StringVar()
        light_value_str.set("%s" % light_value)
        lebel2 = tk.Label(window, text="光敏电阻:", fg='black', font=('宋体', 30))
        value2 = tk.Label(window, textvariable=light_value_str, fg='black', font=('宋体', 35))
        lebel2.place(x=20, y=80, anchor='nw')
        value2.place(x=200, y=80, anchor='nw')
        
        # 显示光敏电阻 动态变化值
        heat_value_str = tk.StringVar()
        heat_value_str.set("%s" % heat_value)
        lebel3 = tk.Label(window, text="热敏电阻:", fg='black', font=('宋体', 30))
        value3 = tk.Label(window, textvariable=heat_value_str, fg='black', font=('宋体', 35))
        lebel3.place(x=20, y=140, anchor='nw')
        value3.place(x=200, y=140, anchor='nw')


class Data(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        # PCF8591 模块的地址
        # 由命令i2cdetect -y 1查询得到
        self.address = 0x48 

        # 在树莓派中，I2C 设备位于 I2C-1，所以此处的编号为 1 
        self.bus = smbus.SMBus(1)
        # self.control_num = control_num

    def run(self):
        global show_value, light_value, heat_value
        print("Starting " + self.name)
        while True:
            # 热敏电阻
            self.bus.write_byte(self.address,0x40)
            heat_value = self.bus.read_byte(self.address)
            
            # 光敏电阻
            self.bus.write_byte(self.address,0x43)
            light_value = self.bus.read_byte(self.address)
            
            # 可变电阻
            self.bus.write_byte(self.address,0x41)
            show_value = self.bus.read_byte(self.address)
            
            # 更新TK界面
            self.update_TK_value()
            time.sleep(0.5)

    def update_TK_value(self):
        global show_value, light_value, heat_value, show_value_str, light_value_str, heat_value_str, window
        show_value_str.set("%s" % show_value)
        light_value_str.set("%s" % light_value)
        heat_value_str.set("%s" % heat_value)




if __name__ == '__main__':

    # 创建新线程
    # TK
    thread1 = TK(1)
    time.sleep(2)
    
    # 获取数据
    thread2 = Data(2)
    
    # 可变电阻 数码管显示
    variable_control_num = 0
    thread3 = Show(3, bcm_list1, variable_control_num)
    
    # 光敏电阻 数码管显示
    light_control_num = 2
    thread4 = Show(4, bcm_list2, light_control_num)
    
    

    
    # 开启线程
    thread1.start()
    time.sleep(2)
    thread2.start()
    thread3.start()
    thread4.start()

    

    # 等待线程结束
    thread1.join()
    time.sleep(2)
    thread2.join()
    thread3.join()
    thread4.join()
    


    time.sleep(5)
    print("Exiting Main Thread")
    
    GPIO.cleanup()