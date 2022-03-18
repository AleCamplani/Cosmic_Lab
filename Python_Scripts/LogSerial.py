"""
This file logs inputs on a serial port.
You define locaiton of log,
length of log(in events),
and port to listen to
"""

"""
Import libraries:
"""
import serial

"""
Set parameters:
"""
ArduinoPort="COM3"
baudrate=38400
RunEvents=1000 #How many we want to log
Filelocation='Test.txt'
verbose=True
veryVerbose=True

"""
Open file
"""

File = open(Filelocation,"a") #append only

"""
Open port
"""

port = serial.Serial(ArduinoPort, baudrate, timeout=10)

"""
Listen for the measurements:
"""

for i in range(RunEvents):
    try: 
        x=port.readline()[0:-2].decode("utf-8")#[] to get rid of line-change character, we deal with this ourselves. decode to make string out of bytes.
        File.write(x+"\n") #Put into the datalog
    except:
        print("Error in Serial")
        continue
    
    if verbose:
        print("Line "+str(i)+" of "+str(RunEvents))
    
    if veryVerbose:
        print(x) #print in termial, so we can look at it live
        
    if i%10==0: #save once in a while
        File.close()
        File = open(Filelocation,"a") #append only


        
        
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
