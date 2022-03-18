"""
This Script looks at N files, and merges into one coincidence files.
Assumes that the files have the same date
"""


"""
Import packages:
"""

import numpy as np
import matplotlib.pyplot as plt
import CosmicLib as CL


"""
Import data:
"""

plt.close('all')
#filenames=['..\FakeDatafiles\Coicidence3Run4.txt','..\FakeDatafiles\Coicidence3Run3.txt','..\FakeDatafiles\Coicidence2Run2.txt']
#filenames=['..\..\Datafiles\GPSTest\Regular2.txt','..\..\Datafiles\GPSTest\Wifi2.txt']
filenames=['..\..\Datafiles\CosmicLabData\MIL_Coincidence_10_3_22.txt','..\..\Datafiles\CosmicLabData\PRG_Coincidence_10_3_22.txt','..\..\Datafiles\CosmicLabData\CPH_Coincidence_10_3_22.txt']

#locations=['MIL','PRG','CPH']
locations=[1,2,3] #encode as numbers

times=None

plot=True

timeBin=600

plt.close("all")
fig,ax=plt.subplots()
plt.xlabel("time (s)")
plt.ylabel(f"Binned average rate rate for {timeBin}s (Hz)")

Data=[]

for j,f in enumerate(filenames):
    data=np.genfromtxt(f,dtype=str,delimiter=';',skip_header=2,skip_footer=1)
    x=data[:,1]
    
    t=np.zeros(len(x))
    for i in range(len(t)):
        t[i]=CL.readTime(x[i],unit="Seconds")
    
    Data.append(t)
    
    l=np.empty(len(t),dtype='float')
    l[:]=locations[j]
    
    histData=np.zeros(int(np.max(t)/timeBin))

    for i in range(1,len(histData)+1):
        histData[i-1]=np.sum(np.where(np.all([t<i*timeBin,t>=(i-1)*timeBin],axis=0),1,0))

    t_axis=np.arange(len(histData))*timeBin

    ax.plot(t_axis,histData/timeBin,label=locations[j])

    
    tl=np.array([t,l]).T
    print(tl.shape)
    if times is None:
        times=tl
    else:
        times=np.concatenate((times,tl))

plt.legend()

"""
Define parameters
"""

TimeDelta=0.001 #in seconds

Events_sorted=times[times[:,0].argsort()] # Ascending list of times with events

"""
Now we merge, by looking for coincidences within some time-delta
"""


MergedList=[] #list we put results in

PulseEvent=Events_sorted[0,0] #first event in a coincidence
count=1 #How many are within the time-delta
LocationsInPulse=[Events_sorted[0,1]]

for i in range(1,len(Events_sorted)): #look through sorted list
    
    if np.abs(Events_sorted[i,0]-PulseEvent)<TimeDelta: #we are in pulse still
        count+=1 #increment counter
        LocationsInPulse.append(Events_sorted[i,1])
    else: #we must note the just finished pulse(coincidence)
        if count>1:
            time=(Events_sorted[i-1,0]+PulseEvent)/2 #note time in middle as time of pulse
        else:
            time=PulseEvent #no concidence, so note 'pulse' of one event
        
        MergedList.append([count,time,LocationsInPulse]) #put in list of results
        PulseEvent=Events_sorted[i,0] #are in new pulse 
        count=1 #reset counter
        LocationsInPulse=[Events_sorted[i,1]]
        
    if i==len(Events_sorted)-1:#catch last event
        if count>1:
            time=(Events_sorted[i-1,0]+PulseEvent)/2
        else:
            time=PulseEvent
            
        
        MergedList.append([count,time,LocationsInPulse]) 


MergedList=np.array(MergedList,dtype=object)

counts=np.array(MergedList[:,0],dtype=float) # make into numpy array, nicer to work with

print("SHOULD BE 0 : "+str(np.sum(counts[:])-len(times))) #sanity-check(did we lose anyone?, should print 0)

"""
Print out the coincidences:
"""

CoincidencesAcrossFiles=[]

for mEvent in MergedList:
    if mEvent[0]>1:#There is coincidence!
        CoincidencesAcrossFiles.append(mEvent)
        
CoincidencesAcrossFiles=np.array(CoincidencesAcrossFiles)

#print(CoincidencesAcrossFiles)
print(len(CoincidencesAcrossFiles))  
    
"""
Sort to only care about conicidences with all three locations:
"""

candidates=[]

for mEvent in MergedList:
    if mEvent[0]>=3:
        candidates.append(mEvent)

#print(candidates)
print(len(candidates))

AllLocCoinc=[]

for candit in candidates:
    
    hasM=False#1
    hasP=False#2
    hasC=False#3
    
    for loc in candit[2]:
        locINT=int(loc)
        if locINT==1:
            hasM=True
        if locINT==2:
            hasP=True
        if locINT==3:
            hasC=True
        
    if (hasM and hasP and hasC):
        AllLocCoinc.append(candit)
        
AllLocCoinc=np.array(AllLocCoinc)

print(AllLocCoinc[:,1])

"""
The Simple solution:
"""

CP=np.array(CL.Coinc(Data[2],Data[1],TimeDelta))
CM=np.array(CL.Coinc(Data[2],Data[0],TimeDelta))
PM=np.array(CL.Coinc(Data[1],Data[0],TimeDelta))

MPC=np.array(CL.Coinc(Data[0],Data[1][CP[:,1]],TimeDelta))

print(len(MPC))
print(Data[0][MPC[:,0]])



