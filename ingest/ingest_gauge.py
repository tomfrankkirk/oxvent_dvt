import serial, time, io, datetime
import serial.tools.list_ports
import warnings

from oxvent import OxVentLogger

from kbthread import KeyboardThread

from bronk import Bronk

millis = lambda: int(round(time.time() * 1000))


#test params

sample_length_millis = 2000

init_flow = 100

final_flow = 650

diff_flow = 50

zeroing_enabled = 1 #toggles whether we take a zero reading
sweep_enabled = 1 #toggles whether we sweep the range defined above







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


#oxvent.block_gp()
#print("dp blocked")

oxvent.enable()
    
while kb_flag:

    oxvent.mainloop()


print("log stopped, processing")  

oxvent.analyser.process_all()