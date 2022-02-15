"""
This file make plots
"""

"""
Import libraries:
"""
import CosmicLib as CL
import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from scipy import stats
from ExternalFunctions import nice_string_output, add_text_to_ax    # Useful functions to print fit results on figure


plt.close("all")

"""
Set parameters:
"""
#Filelocation='..\..\Datafiles\CosmicLabData\CopenhagenCoincidence090222Clean.txt'
Filelocation='..\..\Datafiles\Gen3Files\Gen3Coincidence12Run1.txt'


#For the histogram:
emin=0-0.5
emax=30+0.5
Nbins=int(emax-emin)
timeBin=1 #in seconds

#For running average:
Running_Average_time=5 #in seconds
min_t=0
max_t=300
points=1000


#Cut out end:
Points=50000

"""
Open file
"""

Data=np.genfromtxt(Filelocation,dtype=str,delimiter=';',skip_header=2,skip_footer=1)

Data=Data[0:Points]

x=Data[:,1] #slice to get times

"""
Convert to seconds:
"""
times=np.zeros(len(x))
for i in range(len(times)):
    
    times[i]=CL.readTime(x[i],unit="Seconds")
times=times-np.min(times)#subtracj starting time

"""
Running average:
"""

averages=np.zeros(points)
averages_times=np.linspace(min_t,max_t,points)

dt=(max_t-min_t)/points

for i in range(len(averages)):
    n=np.sum(np.where(np.all([times<averages_times[i],times>averages_times[i]-Running_Average_time],axis=0),1,0))
    averages[i]=n/(Running_Average_time)


fig,ax=plt.subplots()
ax.plot(averages_times,averages)
plt.xlabel("time (s)")
plt.ylabel(f"Running average rate for {Running_Average_time}s (Hz)")
plt.xlim(Running_Average_time,max_t-Running_Average_time)
plt.ylim(0,30)

plt.title("2 detector coincidences",fontsize=15)

d = {'Average rate in Hz: ' : len(times)/np.max(times)
    }

text = nice_string_output(d, extra_spacing=2, decimals=3)
add_text_to_ax(0.2, 0.8, text, ax, fontsize=15)




plt.savefig('3R2Average.png', dpi=600)



"""
Histogram (poisson)
"""
fig,ax=plt.subplots()
plt.xlabel("events in "+str(timeBin)+"s")
plt.ylabel("Counts")

histData=np.zeros(int(np.max(times)/timeBin))

for i in range(1,len(histData)+1):
    histData[i-1]=np.sum(np.where(np.all([times<i*timeBin,times>=(i-1)*timeBin],axis=0),1,0))

counts,bin_edges,_=plt.hist(histData,bins=Nbins,range=(emin,emax),histtype='step',label='data')
binwidth=bin_edges[1]-bin_edges[0]
bin_values=(bin_edges[1::]+bin_edges[0:-1])/2

Minuit.print_level = 1    # Print result of fits (generally - can also be moved down to each fit instance)

N=sum(counts)

def fitFunc(x,mu):
    
    f=N*binwidth*stats.poisson.pmf(x,mu)
    
    return f

# Defining Chi2 calculation:
def chi2(mu):
    condition=counts>0
    y_fit = fitFunc(bin_values[condition], mu)
    chi2 = np.sum(((counts[condition] - y_fit) / np.sqrt(counts[condition]))**2)
    return chi2


mu_guess=np.mean(averages*timeBin)

minuit_chi2 = Minuit(chi2, mu=mu_guess)
minuit_chi2.errordef = 1.0     # This is the definition for ChiSqaure fits
minuit_chi2.migrad()           # This is where the minimisation is carried out! Put ";" at the end to void output

chi2_value = minuit_chi2.fval            # The value minimised, i.e. Chi2 or -2*LogLikeliHood (LLH) value

# Get number of degrees-of-freedom (Ndof):
N_NotEmptyBin = np.sum(counts > 0)
Ndof_value = N_NotEmptyBin - minuit_chi2.nfit

Prob_value = stats.chi2.sf(chi2_value, Ndof_value) # The chi2 probability given N_DOF degrees of freedom
print(f"Chi2 value: {chi2_value:.1f}   Ndof = {Ndof_value:.0f}    Prob(Chi2,Ndof) = {Prob_value:5.8f}")

x=np.linspace(emin,emax,1000)
x_round=np.round(x)
#plt.figure()
#plt.errorbar(binvalues,counts,yerr=np.sqrt(counts),fmt='.',label="data")
#plt.plot(x,fitFunc(x,mu=mu_guess),label="Guess")
plt.plot(x,fitFunc(x_round,*minuit_chi2.values),label="fit")

plt.legend()


d = {'Chisquare: ' : minuit_chi2.fval,
     'p-value: '   : Prob_value
    }

for name in minuit_chi2.parameters:
    d[name] = [minuit_chi2.values[name], minuit_chi2.errors[name]]

text = nice_string_output(d, extra_spacing=2, decimals=3)
add_text_to_ax(0.5, 0.7, text, ax, fontsize=10)

plt.title("2 detector coincidences",fontsize=15)

plt.savefig('2R2Hist.png', dpi=600)


"""
Binned Rate:
"""

t=np.arange(len(histData))*timeBin

fig,ax=plt.subplots()
ax.plot(t,histData/timeBin)
plt.xlabel("time (s)")
plt.ylabel(f"Binned average rate rate for {timeBin}s (Hz)")

plt.title("2 detector coincidences",fontsize=15)

d = {'Average number in one bin: ' : np.mean(histData)
    }

text = nice_string_output(d, extra_spacing=2, decimals=3)
add_text_to_ax(0.1, 0.9, text, ax, fontsize=15)

plt.savefig('3R2Binned.png', dpi=600)


"""
Time-between histogram:
"""

fig,ax=plt.subplots()

Deltas=times[1::]-times[0:-1]

_=ax.hist(Deltas,range=(0,0.2),bins=100)

plt.xlabel("Time delta (s)")
plt.ylabel("count")

