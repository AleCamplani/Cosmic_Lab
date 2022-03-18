"""
Open specified file and outputs clean data to another file

(For removing lines where there was an error in the serial-connection.)

Criterion for keeping line is that the first part matches some keyword and length is consistent.
"""

import numpy as np


StartFile='..\..\Datafiles\CosmicLabData\CPH-Lifetime-11-03-22.txt'

EndFile  ='..\..\Datafiles\CosmicLabData\CLean-CPH-Lifetime-11-03-22.txt'

Keyword="Lifetime"
ReqLenth=39

Data=np.genfromtxt(StartFile,delimiter='\n',dtype=str)

CleanData=[]

removedPoints=0
File = open(EndFile,"a") #append only


for d in Data:
    if d[0:len(Keyword)]==Keyword and len(d)==ReqLenth:
        CleanData.append(d)
        File.write(d+"\n") #Put into the datalog
        #File.write("Coincidence;"+d[len(Keyword)+1:21]+":000:;"+"\n") #Put into the datalog
    else:
        removedPoints+=1
        print(d)
    
print(f"Removed {removedPoints} lines")

CleanData=np.array(CleanData)

File.close()
