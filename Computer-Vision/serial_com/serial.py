import serial
import config
import sys


class SerialComm():
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = config.SERIAL_PORT
        self.ser.baudrate = config.BAUD_RATE
        self.ser.open()

    def set_rgb(self, rgb_list):
        if self.ser.is_open:
            rgb_str = " ".join(str(v) for v in rgb_list)
            msg_str = f"S {rgb_str}\n"
            msg = msg_str.encode('utf-8')
            self.ser.write(msg)

    def reset_rgb(self):
        msg_str = "R\n"
        msg = msg_str.encode('utf-8')
        self.ser.write(msg)

    def getSerialPort(self):
        return self.ser.name

    def close(self):
        self.ser.close()
