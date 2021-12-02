"""
This file runs a measurement.
You define locaiton of log,
length of measurement(in events),
and port to listen to
"""

"""
Import libraries:
"""
import serial
import numpy as np
import CosmicLib as CL
import matplotlib.pyplot as plt

plt.close("all")

"""
Set parameters:
"""
ArduinoPort="COM5"
baudrate=19200
RunEvents=10 #How many we want to log
Filelocation='..\..\Datafiles\Runtest.txt'
plotting=True
verbose=True
veryVerbose=True

headerconst=2
"""
Open file
"""

File = open(Filelocation,"a") #append only

"""
Prepare array:
"""

Data=np.zeros(RunEvents-1)

"""
Prepare plots
"""
if plotting:
    plt.figure(1)
    plt.xlabel("Time between coincidences (s)")
    plt.ylabel("Number of events")

"""
Open port
"""

port = serial.Serial(ArduinoPort, baudrate, timeout=10)


for i in range(RunEvents+headerconst-1):
    x=port.readline()[0:-2].decode("utf-8")#[] to get rid of line-change character, we deal with this ourselves. decode to make string out of bytes.
    File.write(x+"\n") #Put into the datalog
    if veryVerbose:
        print(x) #print in termial, so we can look at it live
    
    if x[0:11]=="Coincidence":    
        Data[i-headerconst]=CL.readTime(x[12::],unit="Seconds")
    
    if i==1:
        StartTime=CL.readTime(x[20::],unit="Seconds")
    
    if i>headerconst:
        rate,time_deltas,time_run,event_times=CL.findRate(Data,StartTime)
        if verbose:
            print(f"Rate is {rate:.5f}Hz")
            print(f"Time run is {time_run:.5f}s")
    
    if plotting and i>headerconst:
        plt.figure(1)
        plt.hist(time_deltas,bins=int(np.sqrt(len(time_deltas))),range=(0,np.mean(time_deltas)+np.std(time_deltas)*3),color="red")
        plt.pause(0.05)

        


port.write("s".encode("utf-8")); #Tell it stop logging
x=port.readline()[0:-2].decode("utf-8")#Get response

if veryVerbose:
    print(x)

File.write(x+"\n") #Put into the datalog

"""
Close everything:
"""

File.close()
port.close()#VERY important
