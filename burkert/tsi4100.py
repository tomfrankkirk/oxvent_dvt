import serial, time

class TSI4100:
    def __init__(self, port):
        self.port = port
        ports = [
            p.device
            for p in serial.tools.list_ports.comports()   
        ]
        self.ser = serial.Serial(ports[port], 38400, timeout = 1, writeTimeout = 1)
        self.flush()

        self.write("SN\r")
        self.readline()
        self.serial_number = self.readline()
        print("Connected to flow meter: " + self.serial_number)

    def sample_time(self,r):
        """sets the time between samples in ms. range 1 to 1000"""
        r = int(r) #make sure it is an int
        if r > 1000:
            print("Too long!")
            return
        if r < 0:
            print("what?")
            return
        r = int(r)
        msg = "SSR" + str(r).zfill(4) + '\r'
        self.write(msg)

    def flush(self):
        self.ser.reset_input_buffer()

    def ok(self):
        msg = "?\r"
        self.write(msg)
        self.readline()

    def readline(self):
        l = self.ser.readline().strip().decode('ascii')
        print("TSI4100 > " + l)
        return l

    def write(self, msg):
        self.ser.write(msg.encode())
        print("TSI4100 < " + msg)

    def readvals(self):
        j = self.readline()
        a = j.split(',')
        a = list(map(float, a))
        return a
        #print(a)

    def collect_data(self,r):
        """takes r samples worth of data in ascii"""
        r = int(r) #make sure it is an int
        if r > 1000:
            print("Too long!")
            return
        if r < 0:
            print("what?")
            return
        
        r = str(r).zfill(4)
        msg = "DAFxx" + r + '\r'
        #self.ser.reset_input_buffer()
        self.write(msg)
        #print(msg)
        time.sleep(1)
        self.readline()
        a = self.readvals()
        
        return a

