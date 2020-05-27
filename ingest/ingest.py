import serial, time, io, datetime
import serial.tools.list_ports
import warnings

from oxvent import OxVentLogger

from kbthread import KeyboardThread

from bronk import Bronk

millis = lambda: int(round(time.time() * 1000))

print("Welcome to OxVent logger.")

now = datetime.datetime.now()
timestring = now.strftime("%Y-%m-%d-%H-%M-%S")
print ("Current date and time : " + timestring)

filename = "OxVent_" + timestring + ".log"

print("Finding ports...")
ports = [
    p.device
    for p in serial.tools.list_ports.comports()   
]

if not ports:
    raise IOError("No devices found")

print("Devices found:")
i = 0
for p in ports:
    print(str(i) + " - " + p)
    i = i+1
oxvent_port_index = int(input("Please select the OxVent: "))
flow_port_index = int(input("Please select the Flow Meter: "))

if oxvent_port_index == flow_port_index:
    print("Warning: same port selected for OxVent and Flow Meter!")



flow_meter = Bronk(flow_port_index)



oxvent = OxVentLogger(oxvent_port_index, filename) #creates an OxVentLogger, opening its serial port


kb_flag = 1

def my_callback(inp):
    global kb_flag
    #evaluate the keyboard input
    if inp == 'Stop': #stops log
        kb_flag = 0
        print("Stopping.")
    elif inp[0] == 'C': #commands the oxvent directly
        oxvent.write(inp[1:len(inp)] + '\r')




kthread = KeyboardThread(my_callback) #sets us a separate thread to handle keyboard cmds

oxvent.enable_logging('FLOW_RAW')  #enables raw flow logging on the oxvent

oxvent.block_dp() #sets the device into blocked mode

flow_meter.setFlowRate(20000) #sets flow rate to 20000

while flow_meter.establishStability() != 1:
    blocked = 1

oxvent.flush()


while kb_flag == 1:
    oxvent.mainloop()


    

oxvent.analyser.process_all()