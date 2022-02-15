"""
This Script is meant to be run as the same as as taking measurements
"""


"""
Import packages:
"""

import numpy as np
import matplotlib.pyplot as plt
import time

"""
Import data:
"""

plt.close('all')
filename='..\..\Datafiles\Coicidence3Run6.txt' #File currently being written to


"""
Define functions
"""

def readTime(s,unit="Hours"):
    """
    Funtion to read timestamp 's', and return a number for that time, 
    in units chosen by the 'unit' argument
    """
    
    hr=int(s[0:2])
    minutes=int(s[3:5])
    seconds=int(s[6:8])
    milliseconds=int(s[9:12])
    microseconds=int(s[13:16])
    nanoseconds=int(s[17:20])
    time=0 #Variable we return
    
    conversion=np.array([0,0,0,0,0,0],dtype=float)
    
    conversion[0]=1
    conversion[1]=1/60
    conversion[2]=1/(60*60)
    conversion[3]=1/(60*60*1000)
    conversion[4]=1/(60*60*1000000)
    conversion[5]=1/(60*60*1000000000)
    
    if unit=="Hours":
        conversion=conversion
        
    if unit=="Minutes":
        conversion=conversion*60
        
    if unit=="Seconds":
        conversion=conversion*60*60
        
    if unit=="Milliseconds":
        conversion=conversion*60*60*1000
    
    if unit=="Microseconds":
        conversion=conversion*60*60*1000*1000
        
        
    time=hr*conversion[0]+minutes*conversion[1]+seconds*conversion[2]+milliseconds*conversion[3]+microseconds*conversion[4]+nanoseconds*conversion[5]
    
    return time
    
def readData(filename):
    Data=np.genfromtxt(filename,dtype=str,delimiter=';',skip_header=2,skip_footer=0)#Footerskip is so we only look at lines we are sure are completely written
    return Data
    

def findRate(Data):
    
    coincidences=0 #Variable for counting
    time_run=0
    
    gps_times_obtained=[] #list of times when we obtain and lose fix (i.e. when we start/stop logging)
    gps_times_lost=[]
    
    time_deltas=[]
    
    event_times=[]
    
    t0=0
    last_time=0
    
    for data in Data: # Run through the lines
        if data[0]=="GPS Fix obtained at":
            gps_times_obtained.append(readTime(data[1],unit="Seconds"))
            if t0==0:
                t0=readTime(data[1],unit="Seconds")
        if data[0]=="GPS Fix lost at" or data[0]=="Stopping logging session":
            gps_times_lost.append(readTime(data[1],unit="Seconds"))
        
        if data[0]=="Coincidence":
            time=readTime(data[1],unit="Seconds")
            if last_time!=0:    
                time_deltas.append(time-last_time)
            last_time=time
            coincidences+=1
            event_times.append(time-t0)
            
    time_run=readTime(Data[-1][1],unit="Seconds")-gps_times_obtained[0] #Time since start
    
    
    rate=coincidences/time_run
    
    return rate,time_deltas,time_run,event_times

def AverageRate(RunningAverageTime,time_deltas): #Finds average rate over the last RunningAverageTime time
    
    flippedTime=np.flip(time_deltas)
    
    count=0
    totalDelta=0
    for delta in flippedTime:
        totalDelta+=delta
        if totalDelta<RunningAverageTime:
            count+=1
        else:
            break
    return count/RunningAverageTime

"""
Define parameters for loop:
"""

timeout=1#Number of seconds to liveplot for at max
delay=0.1#How much time we wait between each repeat

Data=readData(filename)
rate,time_deltas,time_run,event_times=findRate(Data)

RunningAverage=[]
Times=[]

RunningAverageTime=300

offset=0

for i,delta in enumerate(time_deltas):
    RunningAverage.append(AverageRate(RunningAverageTime,time_deltas[0:i+1]))
    Times.append(event_times[i])
    

lastTime_run=0


plt.figure(1)
plt.xlabel("Time between coincidences (s)")
plt.ylabel("Number of events")

plt.figure(2)
plt.xlabel("Time  since start of logging(s)")
plt.ylabel("Running average of rate over last "+str(RunningAverageTime)+"s")

"""
Run loop:
"""
Start=time.time()
while((time.time()-Start)<timeout):
    Data=readData(filename)
    rate,time_deltas,time_run,event_times=findRate(Data)
    print("Total Average rate: "+str(rate)+"Hz")
    
    plt.figure(1)
    plt.hist(time_deltas,bins=int(np.sqrt(len(time_deltas))),range=(0,np.mean(time_deltas)+np.std(time_deltas)*3),color="red")
    plt.pause(0.05)
    
    if time_run!=lastTime_run: #only update this plot if we have new event
        lastTime_run=time_run
        RunningAverage.append(AverageRate(RunningAverageTime,time_deltas))
        Times.append(time_run)
        
        plt.figure(2)
        plt.plot(Times,RunningAverage,color="blue")
        plt.xlim(RunningAverageTime,np.max(Times))
        plt.pause(0.05)
        
    time.sleep(delay)
    if Data[-1][0]=="Stopping logging session": #Stop liveplotting if we stop logging data
        print("Logging has Stopped")
        break


    
