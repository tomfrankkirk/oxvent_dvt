class Bronk:
    
    currentFlowRate = 0 # Keep track of what the curent flow rate should be
    maxFlowRate = 40000 # ml/min
    bronkUnitsMaxDec = 32000 # Max set-point of the Bronkhorst (corresponds to 4l/min)
    bronkRequestMeasure = ":06030401210120\r\n"
    
    def __init__(self, portName):
        flow_ser = serial.Serial(portName, 38400)
        
    def setFlowRate(flowRate):
    
        # Add a catch of the set point being out of range
        
        # Update the instance variable
        currentFlowRate = flowRate
        
        # Convert ml/s to ml/min
        millilitreMinute = (flowRate * 60)
        # Convert to Bronkhorst units (max range = 32,000) and to hex
        bronkSetPointDec = (millilitreMinute * bronkUnitsMaxDec) / maxFlowRate
        bronkSetPointHex = "%04x" % bronkSetPointDec

        # Generate the command string for the Bronkhorst
        bronkCommand = ":0603010121" + bronkSetPointHex + "\r\n"
    
        flow_ser.write(bronkCommand)
    
        # The Bronkhorst should send an acknowledgement - check that it was successful
        if flow_ser.read(100) != ":0403000005\r\n":
            print "Error sending command to Bronkhorst"
            return{}
        
    def getFlowRate():
        
        # Request a measurement of the flow rate from the Bronkhorst
        flow_ser.write(bronkRequestMeasure)
        measuredHex = flow_ser.read(100)[11:15]
        
        # Convert Bronkhorst units from hex to decimal, and convert to ml/s
        bronkUnitsDec = int(measuredHex, 16)
        flowRate = (bronkUnitsDec * maxFlowRate) / bronkUnitsMaxDec
        
        return flowRate
    
    def establishStability():
        
        correctFlowCounts = 0
        
        # Compare a reading to the set flow rate. if it's in range, increment the counter
        for x in range(0, 5):
            if abs(self.getFlowRate() - flowRate) < 5:
                correctFlowCounts++
        
        # Check that we had 5 successive correct readings
        if correctFlowCounts == 5:
            return True
        else:
            return False
        
        
        
        
        