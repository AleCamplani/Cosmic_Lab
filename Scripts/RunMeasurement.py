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
import time

"""
Set parameters:
"""
ArduinoPort="COM5"
baudrate=19200
RunTime=4 #In seconds
Filelocation='..\..\Datafiles\Runtest.txt'

"""
Open file
"""

File = open(Filelocation,"a") #append only


"""
Open port
"""

port = serial.Serial(ArduinoPort, baudrate, timeout=10)

Start=time.time() #Time we start listening

while ((time.time()-Start)<RunTime): #Run until we run out of time 
    x=port.readline()[0:-2].decode("utf-8")#[] to get rid of line-change character, we deal with this ourselves. decode to make string out of bytes.
    File.write(x+"\n") #Put into the datalog
    print(x) #print in termial, so we cna look at it live
        


port.write("s".encode("utf-8")); #Tell it stop logging
x=port.readline()[0:-2].decode("utf-8")#Get response
print(x)
File.write(x+"\n") #Put into the datalog

"""
Close everything:
"""

File.close()
port.close()#VERY important
