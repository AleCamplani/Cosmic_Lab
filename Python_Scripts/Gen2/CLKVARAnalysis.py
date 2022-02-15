"""
Anyysis of the variation in clockcyckles
"""

"""
Import packages:
"""

import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from scipy import stats

plt.close("all")

"""
Get Data:
"""
filenames=['..\..\Datafiles\CLKVAR4.txt','..\..\Datafiles\CLKVAR3.txt','..\..\Datafiles\CLKVAR2.txt','..\..\Datafiles\CLKVAR1.txt']

rawdata=None

for f in filenames:
    read=np.genfromtxt(f,dtype=str,delimiter=';',skip_header=2,skip_footer=1)
    numbers=np.array(read[:,1],dtype=float)
    if rawdata is None:
        rawdata=numbers
    else:
        rawdata=np.concatenate((rawdata,numbers))

rawdata=np.array(rawdata)

data=rawdata[np.abs(rawdata-np.median(rawdata))<30000]

"""
Plot hist
"""


fig,ax=plt.subplots()

counts,binedges,_=ax.hist(data-np.median(data),range=(-10000,10000),bins=100)

binvalues=(binedges[0:-1]+binedges[1::])/2
binwidth=binedges[1]-binedges[0]

plt.xlabel("# of clock-cycles in second minus median")
plt.ylabel("count")

x=np.linspace(-10000,10000,1000)

ax.plot(x,binwidth*np.sum(counts)*stats.norm.pdf(x,loc=0,scale=np.std(data,ddof=1)))

print(np.std(data,ddof=1))

plt.savefig("CLKVARFig1.png", dpi=600)

"""
Plot difference form last:
"""

Deltas=data[1::]-data[0:-1]

fig,ax=plt.subplots()

counts,binedges,_=ax.hist(Deltas,range=(-10000,10000),bins=100)

binvalues=(binedges[0:-1]+binedges[1::])/2
binwidth=binedges[1]-binedges[0]


plt.xlabel("# of clock-cycles difference from last second")
plt.ylabel("count")

ax.plot(x,binwidth*np.sum(counts)*stats.norm.pdf(x,loc=0,scale=np.std(Deltas,ddof=1)))

print(np.std(Deltas,ddof=1))

plt.savefig("CLKVARFig2.png", dpi=600)

