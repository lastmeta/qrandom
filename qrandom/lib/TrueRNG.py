#!/usr/bin/python

# TrueRNG Read - Simple Example
# Chris K Cockrum
# 8/21/2016
#
# Requires Python 2.7, pyserial
# On Linux - may need to be root or set /dev/tty port permissions to 666
#
# Python 2.7.xx is available here: https://www.python.org/
# Install Pyserial package with:   python -m pip install pyserial

import serial
import time
from bitstring import BitArray
from serial.tools import list_ports

class TrueRNG(object):
    """docstring for [object Object]."""
    def __init__(self, blocksize=102400, numloops=10, rng_com_port='default'):
        self.blocksize = blocksize
        self.numloops = numloops

        def _look_for_port(available_port, name="TrueRNG"):
            rng_com_port = None
            for temp in ports_avaiable:
                if temp[1].startswith(name):
                    if rng_com_port == None:        # always chooses the 1st TrueRNG found
                        return str(temp[0]), str(temp[0])
            return None, None

        # Print our header
        if rng_com_port == 'default':
            ports=dict()
            ports_avaiable = list(list_ports.comports())
            rng_com_port = None
            # Loop on all available ports to find TrueRNG
            rng_com_port, self.rng_com_port = _look_for_port(ports_avaiable, name="TrueRNG")
            if rng_com_port == None:
                rng_com_port, self.rng_com_port = _look_for_port(ports_avaiable, name="USB Serial Device")
        else:
            self.rng_com_port = rng_com_port

        # Print which port we're using
        #print(self.rng_com_port)


    def generate(self):
        # Try to setup and open the comport
        try:
            ser = serial.Serial(port=self.rng_com_port,timeout=10)  # timeout set at 10 seconds in case the read fails
        except:
            print('Port Not Usable!')
            print('Do you have permissions set to read ' + self.rng_com_port + ' ?')
        # Open the serial port if it isn't open
        if(ser.isOpen() == False):
            ser.open()
        # Set Data Terminal Ready to start flow
        ser.setDTR(True)
        # This clears the receive buffer so we aren't using buffered data
        ser.flushInput()
        # Keep track of total bytes read
        totalbytes=0
        bytes = []
        # Loop
        for _ in range(self.numloops):

            # Try to read the port and record the time before and after
            try:
                #before = time.time()    # in microseconds
                x=ser.read(self.blocksize)   # read bytes from serial port
                #after = time.time()     # in microseconds
            except:
                print('Read Failed!!!')
                break

            # Update total bytes read
            totalbytes += len(x)

            # If we were able to open the file, write to disk
            bx = BitArray(x).bin
            bytes.append(bx)

            # Calculate the rate
            #rate=float(self.blocksize) / ((after-before)*1000.0)

            #print(str(totalbytes) + ' Bytes Read at ' + '{:6.2f}'.format(rate) + ' Kbytes/s')

        # Close the serial port
        ser.close()

        #bits = []
        #for byte in bytes:
        #    bit = BitArray(byte)
        #    bits.append(bit.bin)

        return bytes


    def generate_bits(self):
        # Try to setup and open the comport
        try:
            # timeout set at 10 seconds in case the read fails
            ser = serial.Serial(port=self.rng_com_port, timeout=10)
        except:
            print('Port Not Usable!')
            print('Do you have permissions set to read ' + self.rng_com_port + ' ?')
        # Open the serial port if it isn't open
        if ser.isOpen() is False:
            ser.open()
        # Set Data Terminal Ready to start flow
        ser.setDTR(True)
        # This clears the receive buffer so we aren't using buffered data
        ser.flushInput()
        # Keep track of total bytes read
        bits = ser.read(self.blocksize)   # read bytes from serial port
        bits = BitArray(bits).bin
        # Close the serial port
        ser.close()
        return bits

#a = TrueRNG(102400, 1)
#b = a.generate()
#print(b)
