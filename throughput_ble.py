#/usr/bin/python

import serial
import time
import sys

DEFAULT_BAUD = 115200
SEND_SIZE = 100

def addPath(file):
    pth, fl = os.path.split(__file__)
    return os.path.join(pth, file)

def is_number(s):
    try:
        int(s, 16)
        return True
    except:
        return False

class SerialReader():

    def __init__(self, portRx, portTx):
        self.portTx = portTx
        self.portRx = portRx
        self.start_time__sec = time.time()
        self.interval__sec = 0
        self.buffer = []

        self.sendtext = ''.join([str(i) for i in range(SEND_SIZE)])

        self.portTx.write(self.sendtext)
        print self.sendtext

    def didDataArrive(self):

        # Read port
        self.buffer.extend(list(self.portRx.read(1024)))

        # Step through the buffer byte and byte and see if the tick text
        # is at the front.
        while len(self.buffer) >= len(self.sendtext):
            if self.buffer[:len(self.sendtext)] == self.sendtext:

                # Discard the tick text
                self.buffer = self.buffer[len(self.sendtext):]

                # Record time
                snapshot__sec = time.time()
                self.interval__sec = snapshot__sec - self.start_time__sec
                self.start_time__sec = snapshot__sec

                # send another batch of data
                self.portTx.write(self.sendtext)
                return True

            else:
                self.buffer.pop(0)

        return False

def main(port1, port2, baudrate1 = DEFAULT_BAUD, baudrate2 = DEFAULT_BAUD):
    try:
        import serial
    except:
        traceback.print_exc()
        print "="*60
        print "You need to install PySerial"
        print "Windows: easy_install pyserial"
        print "Mac/Linux: sudo easy_install pyserial"

    try:
        s1 = serial.Serial(port1, baudrate1, timeout = 0)
        s2 = serial.Serial(port2, baudrate2, timeout = 0)
        print "Loading serial ports"
    except:
        print "Serial port error"
        exit()

    plot_stop = False

    dataread = SerialReader(s2, s1)

    try:
        while plot_stop == False:
            if dataread.didDataArrive():
                print dataread.interval__sec

    except KeyboardInterrupt:
        print "Keyboard Interrupt"
        plot_stop = True

    finally:
        print "Closing"
        s1.close()
        s2.close()

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print "Usage: python extract_data.py phonelink_serialport phonelinkclient_serialport [baudrate1] [baudrate2]"
    else:
        main(*sys.argv[1:])
