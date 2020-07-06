import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


bcm_number = [17,18,27,22,23,24,25,4]
for bcm_number_ in bcm_number:
    GPIO.setup(bcm_number_, GPIO.OUT)

# HIGH 是灭
# LOW  是亮

# 全部灭
def turn_off_all(bcm_number):
    for i, item in enumerate(bcm_number):
        GPIO.output(item, GPIO.HIGH)

# 效果1 从右到左依次点亮起，从左往右依次熄灭
def task1(bcm_number):
    times = 0
    while times < 5:
        for i, item in enumerate(bcm_number):
            GPIO.output(item, GPIO.LOW)
            time.sleep(0.1)
        for i, item in enumerate(bcm_number[::-1]):
            GPIO.output(item, GPIO.HIGH)
            time.sleep(0.1)
        times += 1


# 效果2 从右到左依次闪烁, 从左到右依次闪烁
def task2(bcm_number):
    times = 0
    while times < 5:
        for i, item in enumerate(bcm_number):
            GPIO.output(item, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(item, GPIO.HIGH)
        for i, item in enumerate(bcm_number[::-1]):
            GPIO.output(item, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(item, GPIO.HIGH)
        times += 1

# 全部一起闪烁
def task3(bcm_number):
    times = 0
    while times < 5:
        for i, item in enumerate(bcm_number):
            GPIO.output(item, GPIO.LOW)
        time.sleep(0.5)
        for i, item in enumerate(bcm_number):
            GPIO.output(item, GPIO.HIGH)
        time.sleep(0.5)
        times += 1
            
            



if __name__ == '__main__':
    turn_off_all(bcm_number)
    task1(bcm_number)
    task2(bcm_number)
    task3(bcm_number)
    GPIO.cleanup()
    



# while True:

        
# 效果3

# sleep(3)
# GPIO.cleanup()
# print("end")