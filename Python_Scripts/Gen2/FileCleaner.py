"""
Open specified file and outputs clean data another file

(For removing lines where there was an error in the serial-connection.)
"""

import numpy as np


StartFile='..\..\Datafiles\CosmicLabData\prague-2022-02-09.txt'

EndFile  ='..\..\Datafiles\CosmicLabData\prague-2022-02-09Clean.txt'

Keyword="Time"

Data=np.genfromtxt(StartFile,delimiter='\n',dtype=str)

CleanData=[]

removedPoints=0

File = open(EndFile,"a") #append only


for d in Data:
    if d[0:len(Keyword)]==Keyword:
        CleanData.append(d)
        #File.write(d+"\n") #Put into the datalog
        File.write("Coincidence;"+d[len(Keyword)+1:21]+":000:;"+"\n") #Put into the datalog
    else:
        removedPoints+=1
        print(d)
    
print(f"Removed {removedPoints} lines")

CleanData=np.array(CleanData)

File.close()
