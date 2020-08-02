import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)

#创建一个 pwm 实例，需要两个参数，第一个是 GPIO 引脚号，这里用 2 脚,因为 2 脚与 A Enable 相连。
#第二个是频率(HZ)
pwm = GPIO.PWM(16,80)
pwm2 = GPIO.PWM(10,80)
# 以输出 90%占空比开始
pwm.start(90)
pwm2.start(90)

GPIO.output(20,True)
GPIO.output(21,False)
GPIO.output(9,True)
GPIO.output(11,False)
#  输出 90% 占空比的方波 3 秒，输出 30% 占空比的方波 3秒。如此往复。可以明显看到电机转速的变化。
while True:
    pwm.ChangeDutyCycle(90)
    pwm2.ChangeDutyCycle(90)
    time.sleep(3)
    pwm2.ChangeDutyCycle(30)
    pwm.ChangeDutyCycle(30)
    time.sleep(3)
