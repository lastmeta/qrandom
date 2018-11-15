#!/usr/bin/python
'''
# TrueRNG Read - Simple Example
# Chris K Cockrum
# 8/21/2016
#
# Requires Python 2.7, pyserial
# On Linux - may need to be root or set /dev/tty port permissions to 666
#
# Python 2.7.xx is available here: https://www.python.org/
# Install Pyserial package with:   python -m pip install pyserial
'''

import serial
import time
import numpy as np
from bitstring import BitArray
from serial.tools import list_ports

class TrueRNG(object):
    """ TrueRNG object for reading random bits from the TrueRNG 3 USB device """

    def __init__(self, blocksize=1024, blocksize_type='bytes', return_type='string', port='default'):
        self.set_blocksize(blocksize)
        self.set_blocksize_type(blocksize_type)
        self.set_return_type(return_type)
        self.set_port(port)

    # sets #####################################################################

    def set_blocksize(self, blocksize):
        self.blocksize = blocksize
        return self.blocksize

    def set_blocksize_type(self, blocksize_type):
        self.blocksize_type = blocksize_type
        if blocksize_type.startswith('b'):
            self.blocksize_modulator = 1
        elif blocksize_type.startswith('k'):
            self.blocksize_modulator = 1024
        elif blocksize_type.startswith('m'):
            self.blocksize_modulator = 1024*1024
        else:
            raise 'invalid blocksize_type. options include: [bytes, kilobytes, megabytes]'
        return self.blocksize_type

    def set_return_type(self, return_type='string'):
        self.return_type = return_type
        if not (return_type.startswith('s')
        or blocksize_type.startswith('b')
        or blocksize_type.startswith('a')):
            raise 'invalid return_type. options include: [string, bits, array]'
        return self.return_type

    def set_port(self, rng_com_port='default'):
        def _look_for_port(available_port, name="TrueRNG"):
            rng_com_port = None
            for temp in ports_avaiable:
                if temp[1].startswith(name):
                    # always chooses the 1st TrueRNG found
                    if rng_com_port == None:
                        return str(temp[0]), str(temp[0])
            return None, None

        if rng_com_port == 'default':
            ports=dict()
            ports_avaiable = list(list_ports.comports())
            rng_com_port = None
            # Loop on all available ports to find TrueRNG
            rng_com_port, self.port = _look_for_port(ports_avaiable, name="TrueRNG")
            if rng_com_port == None:
                rng_com_port, self.port = _look_for_port(ports_avaiable, name="USB Serial Device")
        else:
            self.port = rng_com_port

        return self.port

    # gets #####################################################################

    def get_blocksize(self):
        return self.blocksize

    def get_blocksize_type(self):
        return self.blocksize_type

    def get_port(self):
        return self.port

    def get_return_type(self):
        return self.return_type

    # generate #################################################################

    def generate(self, blocksize=None, return_type=None):
        ''' generate and return a bits as bits, string or array '''
        blocksize = blocksize or self.blocksize
        return_type = return_type or self.return_type

        # Try to setup and open the comport
        try:
            # timeout set at 10 seconds in case the read fails
            ser = serial.Serial(port=self.port, timeout=10)
        except:
            print('Port Not Usable!')
            print(f'Do you have permissions set to read {self.port}?')

        # Open the serial port if it isn't open
        if(ser.isOpen() == False):
            ser.open()

        # Set Data Terminal Ready to start flow
        ser.setDTR(True)

        # This clears the receive buffer so we aren't using buffered data
        ser.flushInput()

        # Try to read the port
        success = False
        y = 0
        while not success and y < 10:
            try:
                bits = ser.read(blocksize * self.blocksize_modulator)
                success = True
            except:
                print('Read Failed!!!')
                y += 1

        ser.close()

        # convery if required
        if return_type == 'bits':
            return bits

        # If we were able to open the file, write to disk
        bytes = BitArray(bits).bin

        if return_type == 'array':
            return self.convert_to_array(bytes)
        # as string
        return bytes


    @staticmethod
    def convert_to_array(bitstring: str) -> np.ndarray:
        return np.fromstring(bitstring, 'u1') - ord('0')
