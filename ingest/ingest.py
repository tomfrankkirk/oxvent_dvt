import serial, time, io, datetime
import serial.tools.list_ports
import warnings

from oxvent import OxVentLogger

from kbthread import KeyboardThread


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



flow_ser = serial.Serial(ports[flow_port_index]) #serial device for the TSI Flow Meter



oxvent = OxVentLogger(oxvent_port_index, filename) #creates an OxVentLogger, opening its serial port


main_flag = 1

def my_callback(inp):
    global main_flag
    #evaluate the keyboard input
    if inp == 'S': #stops log
        main_flag = 0
        print("Stopping.")
    elif inp[0] == 'C': #commands the oxvent directly
        oxvent.write(inp[1:len(inp)] + '\r')




kthread = KeyboardThread(my_callback) #sets us a separate thread to handle keyboard cmds

oxvent.enable_logging('FLOW_RAW')  #enables raw flow logging on the oxvent



while main_flag == 1:

    
    #this loop basically runs forever until interrupted with Ctrl-C, constantly logging and if appropriate analysing the data. 
    #if you want the flow meter to do stuff, then put it here with a time based if statement, something like:
    # if (time = something):
    #   flow_ser.write("take a reading")
    #   data = flow_ser.read()
    oxvent.mainloop()

oxvent.analyser.process_all()