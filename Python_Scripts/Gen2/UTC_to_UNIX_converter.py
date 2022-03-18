"""
Script for converting from UTC to unix and printing in a new file
"""

import CosmicLib as CL
import numpy as np
import datetime
import time

filename='..\..\Datafiles\CosmicLabData\MIL_Coincidence_10_3_22.txt'

Endlocation='..\..\Datafiles\CosmicLabData\MIL_Coincidence_10_3_22_UNIX.txt'

Prefix="MIL"

data=np.genfromtxt(filename,dtype=str,delimiter=';',skip_header=2,skip_footer=1)

year=2022
month=3
day=10

print(data)

File = open(Endlocation,"a") #append only

for d in data:
    
    t=CL.readTime(d[1],unit="Seconds")
    
    UNIX=time.mktime(datetime.datetime(year, month, day).timetuple())+int(t)
    
    decimals=t%1
    
    File.write(Prefix+";"+str(int(UNIX))+"."+str(int(decimals.round(9)*10**9))+"\n") #Put into the datalog

File.close()