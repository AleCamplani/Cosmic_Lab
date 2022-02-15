"""
This Script finds the average countrate/time for at given set of coincidence measurements.
"""


"""
Import packages:
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as fit

"""
Define functions
"""

def readTime(s,unit="Hours"):
    """
    Funtion to read timestamp 's', and return a number for that time, 
    in units chosen by the 'unit' argument
    """
    
    hr=int(s[5:7])
    minutes=int(s[8:10])
    seconds=int(s[11:13])
    milliseconds=int(s[14:17])
    microseconds=int(s[18:21])
    
    time=0 #Variable we return
    
    conversion=np.array([0,0,0,0,0],dtype=float)
    
    conversion[0]=1
    conversion[1]=1/60
    conversion[2]=1/(60*60)
    conversion[3]=1/(60*60*1000)
    conversion[4]=1/(60*60*1000000)
    
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
        
        
    time=hr*conversion[0]+minutes*conversion[1]+seconds*conversion[2]+milliseconds*conversion[3]+microseconds*conversion[4]
    
    return time
    
    
def Rate(Data):
    coincidences=0 #Variable for counting
    time_run=0
    
    gps_times_obtained=[] #list of times when we obtain and lose fix (i.e. when we start/stop logging)
    gps_times_lost=[]
    
    for data in Data: # Run through the lines
        if data[0]=="GPS Fix obtained at":
            gps_times_obtained.append(readTime(data[1],unit="Seconds"))
        if data[0]=="GPS Fix lost at" or data[0]=="Stopping logging session":
            gps_times_lost.append(readTime(data[1],unit="Seconds"))
        
        if data[0]=="Coincidence":
            coincidences+=1
            
    
    for i,t_lost in enumerate(gps_times_lost):
        time_run+=t_lost-gps_times_obtained[i]
    
    
    rate=coincidences/time_run
    
    return rate

"""
Import data:
"""

plt.close('all')
filenames=['..\Datafiles\Coicidence1Run2.txt','..\Datafiles\Coicidence1Run3.txt','..\Datafiles\Coicidence1Run4.txt']

A=[41*102,43*80,31*54]
Rates=np.zeros(len(filenames))

for i,filename in enumerate(filenames):    
    Data=np.genfromtxt(filename,dtype=str,delimiter=';',skip_header=2)
    print(Rate(Data)/A[i])
    Rates[i]=Rate(Data)
    
plt.plot(A,Rates,'.')

def StraightLine(x,a,b):
    return a*x+b

val,cov = fit.curve_fit(StraightLine,A,Rates)    
x=np.linspace(0,np.max(A)*1.3,1000)

plt.plot(x,StraightLine(x,*val))
plt.xlabel("Area [square cm]")
plt.ylabel("Rate [Hz]")


print(val)
print(val[1]*40e-9)
print(val[0]*A[0]*40e-9)