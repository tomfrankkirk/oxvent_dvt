class Bronk:
    

    
    def __init__(self, portName):
        self.port = port
        ports = [
            p.device
            for p in serial.tools.list_ports.comports()   
        ]
        self.ser = serial.Serial(ports[port], 115200, timeout = 0)
        
        
        self.currentFlowRate = 0 # Keep track of what the curent flow rate should be
        self.maxFlowRate = 40000 # ml/min
        self.bronkUnitsMaxDec = 32000 # Max set-point of the Bronkhorst (corresponds to 4l/min)
        self.bronkRequestMeasure = ":06030401210120\r\n"
        
    def setFlowRate(self,flowRate):
    
        # Add a catch of the set point being out of range
        
        # Update the instance variable
        self.currentFlowRate = flowRate
        
        # Convert ml/s to ml/min
        millilitreMinute = (flowRate * 60)
        # Convert to Bronkhorst units (max range = 32,000) and to hex
        bronkSetPointDec = (millilitreMinute * bronkUnitsMaxDec) / maxFlowRate
        bronkSetPointHex = "%04x" % bronkSetPointDec

        # Generate the command string for the Bronkhorst
        bronkCommand = ":0603010121" + bronkSetPointHex + "\r\n"
    
        self.write(bronkCommand)
    
        # The Bronkhorst should send an acknowledgement - check that it was successful
        if self.ser.read(100) != ":0403000005\r\n":
            print "Error sending command to Bronkhorst"
            return{}

    def write(self, s):
        self.ser.write(bytes(s,'utf-8'))
        
    def getFlowRate(self):
        
        # Request a measurement of the flow rate from the Bronkhorst
        self.ser.write(bronkRequestMeasure)
        measuredHex = self.ser.read(100)[11:15]
        
        # Convert Bronkhorst units from hex to decimal, and convert to ml/s
        bronkUnitsDec = int(measuredHex, 16)
        flowRate = (bronkUnitsDec * maxFlowRate) / bronkUnitsMaxDec
        
        return flowRate
    
    def establishStability(self):
        
        self.correctFlowCounts = 0
        
        # Compare a reading to the set flow rate. if it's in range, increment the counter
        for x in range(0, 5):
            if abs(self.getFlowRate() - self.currentFlowRate) < 5:
                self.correctFlowCounts +=1
        
        # Check that we had 5 successive correct readings
        if (self.correctFlowCounts == 5):
            self.stable = 1
        else:
            self.stable = 0
        
    def mainloop(self):
        if True:
            
        
        
        
        
        
        