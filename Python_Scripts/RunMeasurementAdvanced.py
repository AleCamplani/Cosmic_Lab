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
ArduinoPort="COM3"
baudrate=38400
RunEvents=1000 #How many we want to log
Filelocation='..\..\Datafiles\Gen3Files\Gen3Coincidence15Run1.txt'
#Filelocation='..\..\Datafiles\Gen3Files\Test.txt'
plotting=False
verbose=True
veryVerbose=False

headerconst=1

emin=30
emax=90
Nbins=emax-emin+1
timeBin=2 #in seconds
histData=[]
n=0
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
    plt.xlabel("events in "+str(timeBin)+"s")
    plt.ylabel("Counts")

"""
Open port
"""

port = serial.Serial(ArduinoPort, baudrate, timeout=10)


for i in range(RunEvents+headerconst-1):
    try: 
        x=port.readline()[0:-2].decode("utf-8")#[] to get rid of line-change character, we deal with this ourselves. decode to make string out of bytes.
        if x[0:11]=="Coincidence":    
            Data[i-headerconst]=CL.readTime(x[12::],unit="Seconds")
        
        if i==2:
            StartTime=CL.readTime(x[12::],unit="Seconds")
        File.write(x+"\n") #Put into the datalog
    except:
        print("Error in Serial")
        continue
    
    if veryVerbose:
        print(x) #print in termial, so we can look at it live
    
    
    if i>headerconst:
        rate,time_deltas,time_run,event_times=CL.findRate(Data,StartTime)
        if verbose:
            print(f"Count nr. {i-1} of {RunEvents}")
            print(f"Rate is {rate:.5f}Hz")
            print(f"Time run is {time_run:.5f}s")
    
    if plotting and i>headerconst:
        plt.figure(1)
        
        if n<int(time_run/timeBin): #Only run if we are in new time-interval
            adjusttimes=event_times-n*timeBin #times in range 0 to timeBin are the evetns we are loking for
            histData.append(np.sum(np.where(adjusttimes<timeBin, 1, 0)-np.where(adjusttimes<0, 1, 0))) #append the number of events in the range 0 to timebin
            n+=1
            plt.hist(histData,bins=Nbins,range=(emin,emax),color="red")
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
