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

locations=['MIL','PRG','CPH']

times=None

for f in filenames:
    Data=np.genfromtxt(f,dtype=str,delimiter=';',skip_header=2,skip_footer=1)
    x=Data[:,1]
    
    t=np.zeros(len(x))
    for i in range(len(t)):
        t[i]=CL.readTime(x[i],unit="Seconds")

    if times is None:
        times=t
    else:
        times=np.concatenate((times,t))


"""
Define parameters
"""

TimeDelta=0.00001 #in seconds

Events_sorted=np.sort(times) # Ascending list of times with events

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

print("SHOULD BE 0 : "+str(np.sum(MergedList[:,0])-len(times))) #sanity-check(did we lose anyone?, should print 0)

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
    



