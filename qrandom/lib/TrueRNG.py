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
                or return_type.startswith('b')
                or return_type.startswith('a')):
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
            ports = dict()
            ports_avaiable = list(list_ports.comports())
            rng_com_port = None
            # Loop on all available ports to find TrueRNG
            rng_com_port, self.port = _look_for_port(
                ports_avaiable, name="TrueRNG")
            if rng_com_port == None:
                rng_com_port, self.port = _look_for_port(
                    ports_avaiable, name="USB Serial Device")
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
        if (ser.isOpen() == False):
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


def withinRange1(bit_array, chunk_size=15, max_value=32831):
    # Ensure the bit array length is a multiple of chunk_size
    trim_size = len(bit_array) % chunk_size
    if trim_size != 0:
        bit_array = bit_array[:-trim_size]

    # Reshape the array into chunks of chunk_size
    reshaped_array = bit_array.reshape(-1, chunk_size)

    # Convert each chunk into an integer
    numbers = np.packbits(reshaped_array, axis=-1)

    # Convert from binary to decimal
    numbers = numbers.dot(2**np.arange(chunk_size)[::-1])

    # Filter out numbers greater than max_value
    valid_numbers = numbers[numbers <= max_value]

    return valid_numbers


def withinSpecialRange(bit_array, chunk_size=23):
    '''
    generating random numbers between and including 0 and 32832
    32832 = 32768 + 64
    111111111111111 = 32767
    111111 = 63
    1 = indicator to add 1 to 32767
    1 = indicator to add 1 to 64
    chunk size = 15 + 6 + 1 + 1 
    '''
    def chunk_array(arr, chunk_size):
        # Trim the array if it's not divisible by chunk_size
        trim_size = len(arr) % chunk_size
        if trim_size != 0:
            arr = arr[:-trim_size]
        # Reshape the array into chunks of chunk_size
        return arr.reshape(-1, chunk_size)

    def binary_array_to_int(arr, num_bits, starting_at=0):
        # Ensure starting_at is within the array bounds
        starting_at = max(0, min(starting_at, len(arr) - 1))
        # Ensure num_bits does not exceed the length of the array from the starting point
        num_bits = min(num_bits, len(arr) - starting_at)
        # Select the bits from starting_at to starting_at + num_bits
        selected_bits = arr[starting_at:starting_at + num_bits]
        # Convert the selected binary array to an integer
        int_value = selected_bits.dot(2 ** np.arange(selected_bits.size)[::-1])
        return int_value

    array = chunk_array(bit_array, chunk_size)
    return [
        binary_array_to_int(array[i], 15) +
        binary_array_to_int(array[i], 6, 15) +
        array[i][21] +
        array[i][22]
        for i in range(len(array))]


def generate_70_million_numbers():
    t = TrueRNG(blocksize=1024*1024, return_type='array')
    numbers = []
    while len(numbers) < 70_000_000:
        numbers = numbers + withinSpecialRange(t.generate())
    return numbers[:70_000_000]
