"""
Open specified file and outputs clean data another file

(For removing lines where there was an error in the serial-connection.)
"""

import numpy as np


StartFile='..\..\Datafiles\CosmicLabData\CopenhagenCoincidence090222.txt'

EndFile='..\..\Datafiles\CosmicLabData\CopenhagenCoincidence090222Clean.txt'

Keyword="Coincidence"

Data=np.genfromtxt(StartFile,delimiter='\n',dtype=str)

CleanData=[]

removedPoints=0

File = open(EndFile,"a") #append only


for d in Data:
    if d[0:len(Keyword)]==Keyword:
        CleanData.append(d)
        File.write(d+"\n") #Put into the datalog
    else:
        removedPoints+=1
        print(d)
    
print(f"Removed {removedPoints} lines")

CleanData=np.array(CleanData)

File.close()
