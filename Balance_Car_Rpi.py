import smbus
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)

pwm = GPIO.PWM(16,80)
pwm2 = GPIO.PWM(10,80)

class Gyro(object):

    def __init__(self, addr):
        self.addr = addr
        self.i2c = smbus.SMBus(1)

    def get_gyro(self):
        try:
            self.raw_gyro_x = self.i2c.read_i2c_block_data(self.addr, 0x37, 2)
            self.raw_gyro_y = self.i2c.read_i2c_block_data(self.addr, 0x38, 2)
            self.raw_gyro_z = self.i2c.read_i2c_block_data(self.addr, 0x39, 2)
        except IOError:
            print("ReadError: gyro_gyro")
            return (0, 0, 0)
        else:
            self.k_gyro = 2000
            self.gyro_x = (self.raw_gyro_x[1] << 8 | self.raw_gyro_x[0]) / 32768 * self.k_gyro
            self.gyro_y = (self.raw_gyro_y[1] << 8 | self.raw_gyro_y[0]) / 32768 * self.k_gyro
            self.gyro_z = (self.raw_gyro_z[1] << 8 | self.raw_gyro_z[0]) / 32768 * self.k_gyro

            if self.gyro_x >= self.k_gyro:
                self.gyro_x -= 2 * self.k_gyro

            if self.gyro_y >= self.k_gyro:
                self.gyro_y -= 2 * self.k_gyro

            if self.gyro_z >= self.k_gyro:
                self.gyro_z -= 2 * self.k_gyro

            return (self.gyro_x, self.gyro_y, self.gyro_z)

    def get_angle(self):
        try:
            self.raw_angle_x = self.i2c.read_i2c_block_data(self.addr, 0x3d, 2)
            self.raw_angle_y = self.i2c.read_i2c_block_data(self.addr, 0x3e, 2)
            self.raw_angle_z = self.i2c.read_i2c_block_data(self.addr, 0x3f, 2)
        except IOError:
            print("ReadError: gyro_angle")
            return (0, 0, 0)
        else:
            self.k_angle = 180

            self.angle_x = (self.raw_angle_x[1] << 8 | self.raw_angle_x[0]) / 32768 * self.k_angle
            self.angle_y = (self.raw_angle_y[1] << 8 | self.raw_angle_y[0]) / 32768 * self.k_angle
            self.angle_z = (self.raw_angle_z[1] << 8 | self.raw_angle_z[0]) / 32768 * self.k_angle
            if self.angle_x >= self.k_angle:
                self.angle_x -= 2 * self.k_angle

            if self.angle_y >= self.k_angle:
                self.angle_y -= 2 * self.k_angle

            if self.angle_z >= self.k_angle:
                self.angle_z -= 2 * self.k_angle
            return (self.angle_x, self.angle_y, self.angle_z)

def Motor(speed):
    if(speed>0):
        if(speed>=100):
            speed=100
        pwm.ChangeDutyCycle(speed)
        pwm2.ChangeDutyCycle(speed)
        GPIO.output(20, False)
        GPIO.output(21, True)
        GPIO.output(9, True)
        GPIO.output(11, False)
    elif{speed<0}:
        if(speed<=-100):
            speed=-100
        pwm.ChangeDutyCycle(-speed)
        pwm2.ChangeDutyCycle(-speed)
        GPIO.output(20, True)
        GPIO.output(21, False)
        GPIO.output(9, False)
        GPIO.output(11, True)
    else:
        GPIO.output(20, False)
        GPIO.output(21, False)
        GPIO.output(9, False)
        GPIO.output(11, False)


pwm.start(90)
pwm2.start(90)
head_gyro = Gyro(0x50)
p = 3.4
d = 0.5
midle_Value=2.3
while(True):
        angle=head_gyro.get_angle()
        gyro=head_gyro.get_gyro()
        Motor((midle_Value+angle[0])*p+gyro[0]*d)
        time.sleep(0.02)



