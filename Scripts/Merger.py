"""
This Script looks at N files, and merges into one coincidence files.
Assumes that the files have the same date
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
filenames=['..\FakeDatafiles\Coicidence3Run4.txt','..\FakeDatafiles\Coicidence3Run3.txt','..\FakeDatafiles\Coicidence2Run2.txt']

DataList=[]

for filename in filenames:
    DataOneFile=np.genfromtxt(filename,dtype=str,delimiter=';',skip_header=2)
    DataList.append(DataOneFile)

"""
Define parameters
"""

TimeDelta=0.001 #in seconds

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
    
    
  
def getRate(Data,verbose=False):
    
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
            event_times.append(time)
            
    
    for i,t_lost in enumerate(gps_times_lost):
        time_run+=t_lost-gps_times_obtained[i]
    
    
    rate=coincidences/time_run
    
    if verbose:    
        print("Number of coincidences: "+str(coincidences))
        print("Time Run: "+str(time_run)+"s")
        print("Observed Rate: "+str(rate)+"Hz")
        
    return rate,event_times,t0,coincidences
  
    
"""
Now we parse the data,
and combine into one large list of all events(all files)
"""

Events=np.array([])
Counts=[]

for Data in DataList:
    rate,event_times,t0,counts=getRate(Data)
    Events=np.concatenate([Events,event_times])
    Counts.append(counts)

Events_sorted=np.sort(Events) # Ascending list of times with events

"""
Now we merge, by looking for coincidences within some time-delta
"""


MergedList=[] #list we put results in

PulseEvent=Events_sorted[0] #first event in a coincidence
count=1 #How many are within the time-delta


for i in range(1,len(Events_sorted)): #look through sorted list
    
    if np.abs(Events_sorted[i]-PulseEvent)<TimeDelta: #we are in pulse still
        count+=1 #increment counter
    else: #we must note the just finished pulse(coincidence)
        if count>1:
            time=(Events_sorted[i-1]+PulseEvent)/2 #note time in middle as time of pulse
        else:
            time=PulseEvent #no concidence, so note 'pulse' of one event
        
        MergedList.append([count,time]) #put in list of results
        PulseEvent=Events_sorted[i] #are in new pulse 
        count=1 #reset counter
        
    if i==len(Events_sorted)-1:#catch last event
        if count>1:
            time=(Events_sorted[i-1]+PulseEvent)/2
        else:
            time=PulseEvent
        
        MergedList.append([count,time]) 


MergedList=np.array(MergedList) # make into numpy array, nicer to work with

print("SHOULD BE 0 : "+str(np.sum(MergedList[:,0])-np.sum(Counts))) #sanity-check(did we lose anyone?, should print 0)

"""
Print out the coincidences:
"""

CoincidencesAcrossFiles=[]

for mEvent in MergedList:
    if mEvent[0]>1:#There is coincidence!
        CoincidencesAcrossFiles.append(mEvent)
        
CoincidencesAcrossFiles=np.array(CoincidencesAcrossFiles)

print(CoincidencesAcrossFiles)
print(len(CoincidencesAcrossFiles))  
    



