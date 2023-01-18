import time

import adafruit_bus_device.i2c_device as i2c_device
from micropython import const

__version__ = "0.0.0-audo.0"
__repo__ = ""

# default i2c address
EAAPMST_I2CADDR = (0x44)

# Register Addresses

PRODUCT_ID = (0x0)
CFG = (0x1)
INTERRUPT = (0x2)
PS_LT = (0X3)
PS_HT = (0X4)
ALS_TH1 = (0X5)
ALS_TH2 = (0X6)
ALS_TH3 = (0x7)
PS_DATA = (0x8)
ALS_DT1 = (0x9)
ALS_DT2 = (0xA)
ALS_RNG = (0xB)

class AmbProx_Lib:
    """Driver for EAAPMST3923A2 Ambient light and proximity sensor"""

    def __init__(self, i2c, address=EAAPMST_I2CADDR):
        self._i2c = i2c_device.I2CDevice(i2c,address)
        self._buffer = bytearray(1)

    def _write_register_byte(self, register, value):
        with self._i2c:
            self._i2c.write(bytes([register, value]))

    def _read_register_bytes(self, register, result, length=None):
        if length is None:
            length = len(result)
        with self._i2c:
            self._i2c.write_then_readinto(bytes([register]), result, in_end=length)

    def enable_als(self):
        self._write_register_byte(CFG, 0x04)

    def enable_ps(self, interval):
        if (interval == 0): self._write_register_byte(CFG, 0x80) # 800ms pulse
        elif interval == 1: self._write_register_byte(CFG, 0x90) # 400ms pulse
        elif interval == 2: self._write_register_byte(CFG, 0xA0) # 200ms pulse
        elif interval == 3: self._write_register_byte(CFG, 0xB0) # 100ms pulse
        elif interval == 4: self._write_register_byte(CFG, 0xC0) # 75ms  pulse
        elif interval == 5: self._write_register_byte(CFG, 0xD0) # 50ms  pulse
        elif interval == 6: self._write_register_byte(CFG, 0xE0) # 12.5ms pulse
        elif interval == 7: self._write_register_byte(CFG, 0xF0) # continuous
        else: self._write_register_byte(CFG, 0xB0) # 100ms pulse
    
    def set_range(self, val):
        if val == 0: self._write_register_byte(ALS_RNG, 0x00)   # 800 lux range
        elif val == 1: self._write_register_byte(ALS_RNG, 0x01) # 400 lux range
        elif val == 2: self._write_register_byte(ALS_RNG, 0x02) # 200 lux range
        elif val == 3: self._write_register_byte(ALS_RNG, 0x03) # 100 lux range
        elif val == 4: self._write_register_byte(ALS_RNG, 0x04) # 50  lux range
        else: self._write_register_byte(ALS_RNG, 0x00) # default of 800lux range
    
    def get_range(self):
        self._read_register_bytes(ALS_RNG, self._buffer)
        return self._buffer

    # upper 8 bits of Ambient Light range
    def alsdata8(self):
        self._read_register_bytes(ALS_DT1, self._buffer)
        return self._buffer

    def psdata(self):
        self._read_register_bytes(PS_DATA, self._buffer)
        return self._buffer
