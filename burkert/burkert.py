

import serial, time, io, datetime
import serial.tools.list_ports
import re
import csv
import statistics
import psu

import tsi4100

millis = lambda: int(round(time.time() * 1000))



current_delta = 10 # 10mA increments
current_init = 10
current_max = 1000

print("Welcome to Burkert Valve tester.")

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

flow_port_index = 0#int(input("Please select the Flow Meter (typically USB0): "))

flow_meter = tsi4100.TSI4100(flow_port_index)
flow_meter.ok()
flow_meter.sample_time(10)
flow_meter.readline()

power_supply = psu.RSPD_3303C()

power_supply.set_voltage(24)


tag = input("What is the name of this test? Only use underscores? ")

filename = "Burkert_" + timestring + "_" + tag + ".csv"


with open(filename, 'a') as file:
    print(filename)
    writer = csv.writer(file)

    for i in range(current_init,current_max,current_delta):
        
        power_supply.set_current(i)
        power_supply.turn_on()
        time.sleep(2)
        f_all = flow_meter.collect_data(100)

        f = statistics.mean(f_all)
        dat = [i, f]
        writer.writerow(dat)
        power_supply.turn_off()
        time.sleep(1)

print("done")
                    