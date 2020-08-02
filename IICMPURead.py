import smbus
import time
 
 
class Gyro(object):
 
    def __init__(self, addr):
        self.addr = addr
        self.i2c = smbus.SMBus(1)
 
    def get_acc(self):
        try:
            self.raw_acc_x = self.i2c.read_i2c_block_data(self.addr, 0x34, 2)
            self.raw_acc_y = self.i2c.read_i2c_block_data(self.addr, 0x35, 2)
            self.raw_acc_z = self.i2c.read_i2c_block_data(self.addr, 0x36, 2)
        except IOError:
            print("ReadError: gyro_acc")
            return (0, 0, 0)
        else:
            self.k_acc = 16 * 9.8
 
            self.acc_x = (self.raw_acc_x[1] << 8 | self.raw_acc_x[0]) / 32768 * self.k_acc
            self.acc_y = (self.raw_acc_y[1] << 8 | self.raw_acc_y[0]) / 32768 * self.k_acc
            self.acc_z = (self.raw_acc_z[1] << 8 | self.raw_acc_z[0]) / 32768 * self.k_acc
            if self.acc_x >= self.k_acc:
                self.acc_x -= 2 * self.k_acc 
        
            if self.acc_y >= self.k_acc:
               self.acc_y -= 2 * self.k_acc
                
            if self.acc_z >= self.k_acc:
                self.acc_z -= 2 * self.k_acc
            return (self.acc_x, self.acc_y, self.acc_z)
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
def main():
    head_gyro = Gyro(0x50)
    while(True):
        print(" Acc:  " + repr(head_gyro.get_acc()) + "\n", "Gyro: " + repr(head_gyro.get_gyro()) + "\n", "Angle:" + repr(head_gyro.get_angle()) + "\n")
        time.sleep(0.2)
main()

