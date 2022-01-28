"""
Histogram plotter for the lifetime measurement
"""

"""
Import packages:
"""

import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from scipy import stats

"""
Import data:
"""

plt.close('all')
#filenames=['..\..\Datafiles\Lifetime1.txt','..\..\Datafiles\Lifetime2.txt','..\..\Datafiles\Lifetime3.txt']
#filenames=['..\..\Datafiles\Lifetime4.txt']
#filenames=['..\..\Datafiles\Gen3Files\Gen3LifetimeRun1.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun2.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun3.txt']
#filenames=['..\..\Datafiles\Gen3Files\Gen3LifetimeRun4.txt']
#filenames=['..\..\Datafiles\Gen3Files\Gen3LifetimeRun5.txt']
#filenames=['..\..\Datafiles\Gen3Files\Gen3LifetimeRun6.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun5.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun7.txt']
#filenames=['..\..\Datafiles\Gen3Files\Gen3LifetimeRun15.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun14.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun13.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun12.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun11.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun10.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun8.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun9.txt']
#filenames=['..\..\Datafiles\Gen3Files\Gen3LifetimeRun10.txt']
#filenames=['..\..\Datafiles\CosmicLabData\Gen3LifetimeRun16.txt','..\..\Datafiles\Gen3Files\Gen3LifetimeRun10.txt']
#filenames=['..\..\Datafiles\CosmicLabData\Gen3LifetimeRun17.txt']
filenames=['..\..\Datafiles\CosmicLabData\Gen3LifetimeRun18.txt','..\..\Datafiles\CosmicLabData\Gen3LifetimeRun17.txt']


times=None

for f in filenames:
    Data=np.genfromtxt(f,dtype=str,delimiter=';',skip_header=2,skip_footer=1)
    t=np.array(Data[:,2],dtype=float)
    if times is None:
        times=t
    else:
        times=np.concatenate((times,t))
print(np.mean(times))
print(np.min(times))
print(np.max(times))
"""
Plot part of the data
"""

tmin=1800
tmax=25000
#tmin=500
#tmax=2000
Nbins=int(((tmax-tmin)/62.5)/2)

counts,binedges,_=plt.hist(times,bins=Nbins,range=(tmin,tmax),label="Data")

N=np.sum(counts)

binvalues=(binedges[1::]+binedges[0:-1])/2
binwidth=binvalues[1]-binvalues[0]
print(binvalues)
"""
Fit:
"""

Minuit.print_level = 1    # Print result of fits (generally - can also be moved down to each fit instance)

def fitFunc(x,x0,tau,N_B):
    
    f=binwidth*N_B/(binvalues[-1]-binvalues[0])+binwidth*(N-N_B)*np.exp(-(x-x0)/tau)/tau
    
    return np.where(x>x0,f,0)

# Defining Chi2 calculation:
def chi2(x0,tau,N_B):
    condition=np.all([counts>0,binvalues>x0],axis=0)
    condition=counts>0
    y_fit = fitFunc(binvalues[condition], x0,tau,N_B)
    chi2 = np.sum(((counts[condition] - y_fit) / np.sqrt(counts[condition]))**2)
    return chi2


x0_guess=1400
tau_guess=2200
N_B_guess=17000

#x0_guess=0
#tau_guess=2200
#N_B_guess=0


minuit_chi2 = Minuit(chi2, x0=x0_guess,tau=tau_guess,N_B=N_B_guess)
minuit_chi2.errordef = 1.0     # This is the definition for ChiSqaure fits
minuit_chi2.migrad()           # This is where the minimisation is carried out! Put ";" at the end to void output

chi2_value = minuit_chi2.fval            # The value minimised, i.e. Chi2 or -2*LogLikeliHood (LLH) value

# Get number of degrees-of-freedom (Ndof):
N_NotEmptyBin = np.sum(counts > 0)
Ndof_value = N_NotEmptyBin - minuit_chi2.nfit

Prob_value = stats.chi2.sf(chi2_value, Ndof_value) # The chi2 probability given N_DOF degrees of freedom
print(f"Chi2 value: {chi2_value:.1f}   Ndof = {Ndof_value:.0f}    Prob(Chi2,Ndof) = {Prob_value:5.8f}")

print(f"Lifetime from fit: {minuit_chi2.values['tau']:.0f} +- {minuit_chi2.errors['tau']:.0f}ns")

x=np.linspace(tmin,tmax,1000)
fig,ax=plt.subplots()
plt.errorbar(binvalues,counts,yerr=np.sqrt(counts),fmt='.',label="data")
#plt.plot(x,fitFunc(x,x0=x0_guess,tau=tau_guess,N_B=N_B_guess),label="Guess")
plt.plot(x,fitFunc(x,*minuit_chi2.values),label="fit")

plt.xlabel("start-stop (ns)")
plt.ylabel("count")

#plt.legend()
plt.ylim(0,np.max(counts)*1.3)

print(minuit_chi2.values)
print(N-minuit_chi2.values['N_B'])

from ExternalFunctions import nice_string_output, add_text_to_ax    # Useful functions to print fit results on figure

d = {'Chisquare: ' : minuit_chi2.fval,
     'p-value: '   : Prob_value,
     'N'           : N
    }

for name in minuit_chi2.parameters:
    d[name] = [minuit_chi2.values[name], minuit_chi2.errors[name]]

text = nice_string_output(d, extra_spacing=2, decimals=3)
add_text_to_ax(0.4, 0.85, text, ax, fontsize=10)

plt.title("Muon Lifetime",fontsize=15)

plt.savefig('Lifetime.png', dpi=600)


"""
Plot raw data
"""

plt.figure()
tmin=0
tmax=25000
bins=int(((tmax-tmin)/62.5))
_=plt.hist(times,bins=bins,range=(tmin,tmax),label="Data")

plt.figure()
_=plt.hist(times,bins=1000,range=(5000,6000))
