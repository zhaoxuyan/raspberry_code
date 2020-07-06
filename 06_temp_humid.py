#coding: utf-8

from smbus2 import SMBus
import time
import threading
import Tkinter as tk
import RPi.GPIO as GPIO

bus_number  = 1
i2c_address = 0x76

bus = SMBus(bus_number)

digT = []
digP = []
digH = []

t_fine = 0.0

pressure = 0
temperature = 0
var_h = 0
pressure_str, temperature_str, var_h_str = "", "", ""

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
                self.led_show(int(temperature))
            # 光敏电阻
            elif self.control_num == 2:
                time.sleep(0.00001)
                self.led_show(int(var_h))
        
        
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
            
def writeReg(reg_address, data):
    bus.write_byte_data(i2c_address,reg_address,data)

# 得到校准的参数
def get_calib_param():
    calib = []
    
    for i in range (0x88,0x88+24):
        calib.append(bus.read_byte_data(i2c_address,i))
    calib.append(bus.read_byte_data(i2c_address,0xA1))
    for i in range (0xE1,0xE1+7):
        calib.append(bus.read_byte_data(i2c_address,i))

    digT.append((calib[1] << 8) | calib[0])
    digT.append((calib[3] << 8) | calib[2])
    digT.append((calib[5] << 8) | calib[4])
    digP.append((calib[7] << 8) | calib[6])
    digP.append((calib[9] << 8) | calib[8])
    digP.append((calib[11]<< 8) | calib[10])
    digP.append((calib[13]<< 8) | calib[12])
    digP.append((calib[15]<< 8) | calib[14])
    digP.append((calib[17]<< 8) | calib[16])
    digP.append((calib[19]<< 8) | calib[18])
    digP.append((calib[21]<< 8) | calib[20])
    digP.append((calib[23]<< 8) | calib[22])
    digH.append( calib[24] )
    digH.append((calib[26]<< 8) | calib[25])
    digH.append( calib[27] )
    digH.append((calib[28]<< 4) | (0x0F & calib[29]))
    digH.append((calib[30]<< 4) | ((calib[29] >> 4) & 0x0F))
    digH.append( calib[31] )
    
    for i in range(1,2):
        if digT[i] & 0x8000:
            digT[i] = (-digT[i] ^ 0xFFFF) + 1

    for i in range(1,8):
        if digP[i] & 0x8000:
            digP[i] = (-digP[i] ^ 0xFFFF) + 1

    for i in range(0,6):
        if digH[i] & 0x8000:
            digH[i] = (-digH[i] ^ 0xFFFF) + 1  

def readData():
    while True:
        data = []
        for i in range (0xF7, 0xF7+8):
            data.append(bus.read_byte_data(i2c_address,i))
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw  = (data[6] << 8)  |  data[7]
        
        compensate_T(temp_raw)
        compensate_P(pres_raw)
        compensate_H(hum_raw)

def compensate_P(adc_P):
    global t_fine, pressure, temperature, var_h, pressure_str, temperature_str, var_h_str, window
    pressure = 0.0
    
    v1 = (t_fine / 2.0) - 64000.0
    v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * digP[5]
    v2 = v2 + ((v1 * digP[4]) * 2.0)
    v2 = (v2 / 4.0) + (digP[3] * 65536.0)
    v1 = (((digP[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8)  + ((digP[1] * v1) / 2.0)) / 262144
    v1 = ((32768 + v1) * digP[0]) / 32768
    
    if v1 == 0:
        return 0
    pressure = ((1048576 - adc_P) - (v2 / 4096)) * 3125
    if pressure < 0x80000000:
        pressure = (pressure * 2.0) / v1
    else:
        pressure = (pressure / v1) * 2
    v1 = (digP[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
    v2 = ((pressure / 4.0) * digP[7]) / 8192.0
    pressure = pressure + ((v1 + v2 + digP[6]) / 16.0)  
    
    print "pressure : %7.2f hPa" % (pressure/100)
    pressure_ = "%7.2f" % (pressure/100)
    pressure = float(pressure_)
    # 更新tk界面
    setTkValue()
    time.sleep(0.5)
    

def compensate_T(adc_T):
    global t_fine, pressure, temperature, var_h, pressure_str, temperature_str, var_h_str, window
    v1 = (adc_T / 16384.0 - digT[0] / 1024.0) * digT[1]
    v2 = (adc_T / 131072.0 - digT[0] / 8192.0) * (adc_T / 131072.0 - digT[0] / 8192.0) * digT[2]
    t_fine = v1 + v2
    temperature = t_fine / 5120.0


    print "%-6.2f ℃" % (temperature)
    temperature_ = "%-6.2f" % (temperature)
    temperature = float(temperature_)
    # 更新tk界面
    setTkValue()
    time.sleep(0.5)

def compensate_H(adc_H):
    global t_fine, pressure, temperature, var_h, pressure_str, temperature_str, var_h_str, window
    var_h = t_fine - 76800.0
    if var_h != 0:
        var_h = (adc_H - (digH[3] * 64.0 + digH[4]/16384.0 * var_h)) * (digH[1] / 65536.0 * (1.0 + digH[5] / 67108864.0 * var_h * (1.0 + digH[2] / 67108864.0 * var_h)))
    else:
        return 0
    var_h = var_h * (1.0 - digH[0] * var_h / 524288.0)
    if var_h > 100.0:
        var_h = 100.0
    elif var_h < 0.0:
        var_h = 0.0


    print "hum : %6.2f ％" % (var_h)
    var_h_ = "%6.2f" % (var_h)
    var_h = float(var_h_)
    # 更新tk界面
    setTkValue()
    time.sleep(0.5)

def setup():
    osrs_t = 1          #Temperature oversampling x 1
    osrs_p = 1          #Pressure oversampling x 1
    osrs_h = 1          #Humidity oversampling x 1
    mode   = 3          #Normal mode
    t_sb   = 5          #Tstandby 1000ms
    filter = 0          #Filter off
    spi3w_en = 0            #3-wire SPI Disable

    ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
    config_reg    = (t_sb << 5) | (filter << 2) | spi3w_en
    ctrl_hum_reg  = osrs_h

    writeReg(0xF2,ctrl_hum_reg)
    writeReg(0xF4,ctrl_meas_reg)
    writeReg(0xF5,config_reg)


setup()
get_calib_param()

def initialTk():
    global pressure, temperature, var_h, pressure_str, temperature_str, var_h_str, window
    # 气压
    pressure_str = tk.StringVar()
    pressure_str.set("%s" % pressure)
    label1 = tk.Label(window, text="气压: ", fg='black',
                      font=('宋体', 35))
    value1 = tk.Label(window, textvariable=pressure_str,
                      fg='black', font=('宋体', 35))
    label1.place(x=20, y=20, anchor='nw')
    value1.place(x=280, y=20, anchor='nw')

    # 温度
    temperature_str = tk.StringVar()
    temperature_str.set("%s" % temperature)
    label2 = tk.Label(window, text="温度: ", fg='black', font=('宋体', 35))
    value2 = tk.Label(window, textvariable=temperature_str,
                         fg='black', font=('宋体', 35))
    label2.place(x=20, y=80, anchor='nw')
    value2.place(x=280, y=80, anchor='nw')

    # 湿度
    var_h_str = tk.StringVar()
    var_h_str.set("%s" % var_h)
    label3 = tk.Label(window, text="湿度: ",
                            fg='black', font=('宋体', 35))
    value3 = tk.Label(window, textvariable=var_h_str,
                            fg='black', font=('宋体', 35))
    label3.place(x=20, y=140, anchor='nw')
    value3.place(x=280, y=140, anchor='nw')


def tK_Show():
    global pressure, temperature, var_h, pressure_str, temperature_str, var_h_str, window
    window = tk.Tk()  # 第1步，实例化object，建立窗口window
    window.title('window_3')  # 第2步，给窗口的可视化起名字
    window.geometry('1000x600')  # 第3步，设定窗口的大小(长 * 宽)
    initialTk()
    window.mainloop()

def setTkValue():
    global pressure, temperature, var_h, pressure_str, temperature_str, var_h_str, window
    pressure_str.set("%s" % pressure +" hPa")
    temperature_str.set("%s" % temperature+" ℃")
    var_h_str.set("%s" % var_h+" %")

if __name__ == '__main__':
    try:
        # 用于创建TK窗口，并显示对应的值
        thread1 = threading.Thread(target=tK_Show, args=())
        time.sleep(1)
        # 温湿度传感器读数据
        thread2 = threading.Thread(target=readData, args=())
        
        
        # 温度 数码管显示
        variable_control_num = 0
        thread3 = Show(3, bcm_list1, variable_control_num)
        
        # 湿度 数码管显示
        light_control_num = 2
        thread4 = Show(4, bcm_list2, light_control_num)
        
        thread1.start()  # thread1执行
        time.sleep(1)
        thread2.start()  # thread2执行
        thread3.start()
        thread4.start()
        # 等待线程结束
        thread1.join()
        time.sleep(1)
        thread2.join()
        thread3.join()
        thread4.join()
    except KeyboardInterrupt:
        GPIO.cleanup()






