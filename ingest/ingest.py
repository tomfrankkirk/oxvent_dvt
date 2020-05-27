import serial, time, io, datetime
import serial.tools.list_ports
import warnings

from oxvent import OxVentLogger

from kbthread import KeyboardThread

from bronk import Bronk

millis = lambda: int(round(time.time() * 1000))


#test params

sample_length_millis = 5000

init_flow = 100

final_flow = 300

diff_flow = 25









print("Welcome to OxVent logger.")

now = datetime.datetime.now()
timestring = now.strftime("%Y-%m-%d-%H-%M-%S")
print ("Current date and time : " + timestring)



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
oxvent_port_index = int(input("Please select the OxVent (typically ACM0): "))
flow_port_index = int(input("Please select the Flow Meter (typically USB0):: "))

if oxvent_port_index == flow_port_index:
    print("Warning: same port selected for OxVent and Flow Meter!")



flow_meter = Bronk(flow_port_index)

tag = input("What is the name of this test? Only use underscores? :")

filename = "OxVent_" + timestring + "_" + tag + ".log"

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

#oxvent.enable_logging('FLOW_RAW')  #enables raw flow logging on the oxvent
#print("blocking dp")
oxvent.block_dp() #sets the device into blocked mode
#print("dp blocked")
flow_meter.setFlowRate(0)
f = 200

for f in range(init_flow, final_flow, diff_flow):
    flow_meter.setFlowRate(f) #sets flow rate to 20000
    #print("flow rate set")
    while flow_meter.establishStability() != 1:
        blocked = 1
        print("unstable")
    print("flow rate stable")
    oxvent.log_external_flow(f)
    oxvent.flush()
    oxvent.enable()
    
    time_start = millis()
    while millis() < (time_start+sample_length_millis):
        oxvent.mainloop()

    flow_meter.setFlowRate(0)
print("log stopped, processing")  

oxvent.analyser.process_all()