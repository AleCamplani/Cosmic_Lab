"""
This file runs a measurement.
You define locaiton of log,
length of measurement,
and port to listen to
"""

"""
Import libraries:
"""
import serial
import CosmicLib as CL

"""
Set parameters:
"""
ArduinoPort="COM3"
baudrate=19200
RunNumber=50 #How many we want
#Filelocation='..\..\Datafiles\Gen3Files\Gen3LifetimeRun16.txt'
Filelocation='..\..\Datafiles\Gen3Files\Test.txt'


"""
Open file
"""

File = open(Filelocation,"a") #append only


"""
Open port
"""

port = serial.Serial(ArduinoPort, baudrate, timeout=60)

counter=-1

while (counter<RunNumber): #Run until we run out of time 
    x=port.readline()[0:-2].decode("utf-8")#[] to get rid of line-change character, we deal with this ourselves. decode to make string out of bytes.
    
    if counter==1:
        StartTime=CL.readTime(x[9::],unit="Seconds")
    
    if counter>1:
        TRun=CL.readTime(x[9::],unit="Seconds")-StartTime
        print(f"Rate: {counter/TRun:.3f}Hz")
    
    if len(x)>5:#sometimes get an empty string, need to investigate cause. probably timeout
        File.write(x+"\n") #Put into the datalog
        print(x) #print in termial, so we cna look at it live
        counter+=1
        print(f"Measurement {counter} of {RunNumber}")
        


port.write("s".encode("utf-8")); #Tell it stop logging
x=port.readline()[0:-2].decode("utf-8")#Get response
print(x)
File.write(x+"\n") #Put into the datalog

"""
Close everything:
"""

File.close()
port.close()#VERY important
