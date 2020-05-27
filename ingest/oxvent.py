import serial, time, io, datetime
import serial.tools.list_ports
import re
import csv

fourcaps =  re.compile('[A-Z][A-Z][A-Z][A-Z]') #regex to detect 4 letter capital strings

log_dict = {
    'MASTER': 0,
    'FLOW_RAW': 1,
    'FLOW_CALCULATED': 2,
    'ALARM_STATUS': 3,
    'PRESSURE_GAUGE_RAW': 4,
    'PRESSURE_GAUGE_CAL': 5,
    'PRESSURE_DIFF_RAW': 6,
    'PRESSURE_DIFF_CAL': 7,
    'TIDAL_VOLUME': 8, #tidal volume (reports once a cycle)
    'PRESSURE_PEAK': 9,
    'PRESSURE_PEEP': 10
}

set_dict = {
    'IS_VENTILATING': 0,
    'TIDAL_VOLUME': 1
}


class OxVentLogger :
    """Parent class for an oxvent device"""
    def __init__(self, port, filename):
        self.port = port
        ports = [
            p.device
            for p in serial.tools.list_ports.comports()   
        ]
        self.ser = serial.Serial(ports[port], 115200, timeout = 0)



        #self.ser.timeout = 10
        #self.write("0\r") #sends the OxVent an ACK and waits 1 second

        #b1 = self.ser.read()
        #b1 = b1.decode("utf-8")
        #if b1 != '0':
        #    print(b1)
        #    raise IOError("This is not an OxVent!")
        #self.ser.read()
        #self.ser.timeout = 0 #resets to short timeouts
        print("New Oxvent Device instanced.")
        
        
        self.filename = filename
        self.analyser = OxVentAnalyser(filename)

        datafile=open(self.filename, 'a')
        now = datetime.datetime.now()
        timestring = now.strftime("%Y-%m-%d-%H-%M-%S")
        self.summary = "OxVent Log taken on port " + str(ports[port]) + " at " + timestring +'\r'
        datafile.write(self.summary)
        datafile.write("Start of Log:\r")
        datafile.close()

        self.seq = ""
        self.line_count = 1 
        self.extern_line_count = 1

    def __del__(self):
        self.ser.close()

    def write(self, s):
        self.ser.write(bytes(s,'utf-8'))



    def mainloop(self):
        
        data = self.ser.read()
        data = data.decode("utf-8")
        if data != '\n':
            self.seq += data

        
        

        if data == '\r':
            
            now = datetime.datetime.now()
            timestring = now.strftime("%Y-%m-%d-%H-%M-%S")
            linestring = timestring + ",OXVE," + str(self.line_count) + "," + self.seq
            datafile=open(self.filename, 'a')
            datafile.write(linestring)
            datafile.close()
            #print(linestring) 


            self.line_count += 1
            self.seq = ""

    def log_external_flow(self, msg):

        now = datetime.datetime.now()
        timestring = now.strftime("%Y-%m-%d-%H-%M-%S")
        linestring = timestring + ",EXTE," + str(self.extern_line_count) + "," + str(msg) + "\r"
        datafile=open(self.filename, 'a')
        datafile.write(linestring)
        datafile.close()
        print(linestring) 

        self.extern_line_count +=1

    def enable_logging(self, p): 
        """Enables a parameter for logging on the oxvent. Takes a string argument"""
        try:
            message = "1," + str(log_dict[p]) +"\r"
            self.write(message)
        except KeyError:
            print("Key Not Allowed")

    def disable_logging(self, p): 
        """Enables a parameter for logging on the oxvent. Takes a string argument"""
        try:
            message = "2," + str(log_dict[p]) +"\r"
            self.write(message)
        except KeyError:
            print("Key Not Allowed")





    #def clamp(self, n, smallest, largest): return max(smallest, min(n, largest))


class OxVentAnalyser :
    def __init__(self, f):
        self.filename = f
        print("Analyzer attached to " + f)

        self.last_external_val = 0


        self.masterdict = {}  #makes a master dict of lists

    def istag(self,t):  #checks for four letter tags
        return ((len(t) == 4) & bool(fourcaps.match(t)))

    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    
    def parse_line(self, s): #accepts a string s and splits it into bits then parses these into a dict
        s = s.split(',')

        clock_found = 0
        value_found = 0
        
        try:
            linenumber = int(s[2])
        except:
            return{}

        data = dict()  #empty dictionary to store stuff in

        if s[1] == "OXVE": #if data is from an oxvent device

            for num, item in enumerate(s): #retrieves tags and puts them in a dict
                if num < len(s)-1:
                    if self.istag(item) & self.isfloat(s[num+1]):
                        data[item] = float(s[num+1])
        
            clock_found = ('CLOK' in data)

            if not clock_found:
                #print("No timestamp - discarding")
                return {}

            if clock_found:
                return data

        if s[1] == "EXTE": #if data is from an external device
            self.last_external_val = s[3] #stores the last external flow in a buffer
            return {}


    def clear_masterdict(self):
        self.masterdict = {}

    def append_masterdict(self, dict_in):

        #if dict_in != {}:
            #print(dict_in)
            
        clock = dict_in.get('CLOK')

        for key in dict_in:
            if key != 'CLOK':
                newpair = [clock, dict_in.get(key), self.last_external_val]
                if key in self.masterdict: #if we have already had this data point in the dict
                    mainlist = self.masterdict.get(key)
                    mainlist.append(newpair)
                    self.masterdict[key] = mainlist
                else: #if we haven't, make a new key for it in masterdict
                    self.masterdict[key] = [newpair]



    def export_masterdict(self):
        #print(self.masterdict)
        for key in self.masterdict:
            sublist = self.masterdict.get(key)
            with open(self.filename[0:len(self.filename)-4] + "_" + key + ".dat", 'w', newline='') as file:
                print(self.filename[0:len(self.filename)-4] + "_" + key + ".dat")
                writer = csv.writer(file)
                for i in sublist:
                    writer.writerow(i)



    def process_all(self):
        self.clear_masterdict()
        with open(self.filename) as f:
            for cnt, line in enumerate(f):
                #print("Line {}: {}".format(cnt, line),end = '')
                p = self.parse_line(line)
                self.append_masterdict(p)
        self.export_masterdict()








        









        
            
