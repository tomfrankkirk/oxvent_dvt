from universal_usbtmc import import_backend
from universal_usbtmc.exceptions import *
import time

class RSPD_3303C:
    def __init__(self):

        backend = import_backend('linux_kernel')
        self.instrument = backend.Instrument("/dev/usbtmc0")
        print("Connected to power supply:")
        self.identify()
        
        

    def identify(self):
        print(self.instrument.query("*IDN?"))

    def turn_on(self):
        self.instrument.write("OUTP CH1,ON")

    def turn_off(self):
        self.instrument.write("OUTP CH1,OFF")

    def set_voltage(self, v):
        self.instrument.write("CH1:VOLT " + str(v))

    def set_current(self, i):
        self.instrument.write("CH1:CURR " +str(i/1000))


class E36103A:
    def __init__(self):

        backend = import_backend('linux_kernel')
        self.instrument = backend.Instrument("/dev/usbtmc0")
        print("Connected to power supply:")
        self.identify()
        
        

    def identify(self):
        print(self.instrument.query("*IDN?"))

    def turn_on(self):
        self.instrument.write("OUTPut:STATe ON")

    def turn_off(self):
        self.instrument.write("OUTPut:STATe OFF")

    def set_voltage(self, v):
        self.instrument.write("SOUR:VOLT " + str(v))

    def set_current(self, i):
        self.instrument.write("SOUR:CURR " +str(i/1000))





