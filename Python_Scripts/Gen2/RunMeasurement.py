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
ArduinoPort="COM4"
baudrate=38400
RunTime=120 #In seconds
Filelocation='..\..\Datafiles\GPSTest\Regular2.txt'

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
    try:
        x=port.readline()[0:-2].decode("utf-8")#[] to get rid of line-change character, we deal with this ourselves. decode to make string out of bytes.
        File.write(x+"\n") #Put into the datalog
        print(x) #print in termial, so we can look at it live
    except:
        print("Error")
        


port.write("s".encode("utf-8")); #Tell it stop logging
x=port.readline()[0:-2].decode("utf-8")#Get response
print(x)
File.write(x+"\n") #Put into the datalog

"""
Close everything:
"""

File.close()
port.close()#VERY important
