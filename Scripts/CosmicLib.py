"""
Library for Cosmiclab
"""
import numpy as np

def readData(filename):
    Data=np.genfromtxt(filename,dtype=str,delimiter=';',skip_header=2,skip_footer=0)#Footerskip is so we only look at lines we are sure are completely written
    return Data

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


def findRate(Data,StartTime):
      
    t0=StartTime
    
    event_times=Data[Data>0]-t0
    
    coincidences=len(Data[Data>0])
    
    time_deltas=Data[Data>0]-np.roll(Data[Data>0],1)
    
    time_deltas=time_deltas[1::]
    
    time_run=np.max(Data)-t0
    
    rate=coincidences/time_run

    return rate,time_deltas,time_run,event_times