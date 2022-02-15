"""
This Script finds the average countrate/time for at given set of coincidence measurements.
"""


"""
Import packages:
"""

import numpy as np
import matplotlib.pyplot as plt


"""
Import data:
"""

plt.close('all')
filename='..\..\Datafiles\Coicidence3Run5.txt'
Data=np.genfromtxt(filename,dtype=str,delimiter=';',skip_header=2)

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
        

for i,t_lost in enumerate(gps_times_lost):
    time_run+=t_lost-gps_times_obtained[i]


rate=coincidences/time_run

print("Number of coincidences: "+str(coincidences))
print("Time Run: "+str(time_run)+"s")
print("Observed Rate: "+str(rate)+"Hz")

plt.hist(time_deltas,bins=100,range=(0,np.max(time_deltas)))

RunningAverageTime=100*1/rate
Points=100

print(RunningAverageTime)

Times=np.linspace(RunningAverageTime,time_run,Points)
RunningAverage=np.zeros(Points)

lastStop=rate*RunningAverageTime


for i,t in enumerate(Times):
    count=0
    for j in range(np.max([0,int(lastStop-rate*RunningAverageTime)]),len(event_times)):
        if np.abs(t-event_times[j])<RunningAverageTime and t-event_times[j]>0:
            count+=1
        elif event_times[j]-t>0:
            lastStop=j;
            break
    RunningAverage[i]=count/RunningAverageTime
   
plt.figure()
plt.plot(Times,RunningAverage)
plt.xlim(RunningAverageTime,np.max(Times))

