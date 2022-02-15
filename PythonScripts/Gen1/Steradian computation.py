import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

#all in cm, s and sr

flux=6.64e-3

h=40
L5=80
L1=100
W5=41.5
W1=41.5


"""
Old way:
"""


theta=np.pi-2*np.arctan(2*h/(L1+L5))
phi=np.pi-2*np.arctan(2*h/(W1+W5))

sr=2*phi*np.sin(theta/2)

print(sr)
print(theta*180/np.pi)
print(phi*180/np.pi)

sr_est=phi*theta

print(sr_est) # estimate is simply product of the two angles (sides of rectangle on unit sphere)


print(flux*L5*W5*sr)

"""
With integral:
(numerical)
"""

N=100#resolution

w_list=np.linspace(0,W5,N)
l_list=np.linspace(0,L5,N)

delta_L=(L1-L5)/2
delta_W=(W1-W5)/2

dl=L5/N
dw=W5/N

def Omega(l,w):
    alpha_l=np.arctan((l+delta_L)/h)
    beta_l=np.arctan((L5-l+delta_L)/h)
    
    alpha_w=np.arctan((w+delta_W)/h)
    beta_w=np.arctan((W5-w+delta_W)/h)
    
    return (alpha_l+beta_l)*(alpha_w+beta_w)


I=0

Omega_matrix=np.zeros((N,N))

for i,w in enumerate(w_list): #double integral
    for j,l in enumerate(l_list):
        I+=dl*dw*Omega(l,w)
        Omega_matrix[i,j]=Omega(l,w)
        
        
print(np.max(Omega_matrix))
print(I*flux)

plt.imshow(Omega_matrix) # sanity-check


"""
New Method (4/2-22)
"""

N=100

Delta_L=0
Delta_W=0

L_t=80
W_t=41.5

L_b=80
W_b=41.5

h=40 #all in cm


dw_b=W_b/N
dl_b=L_b/N

w_list=np.linspace(0,W_b,N)
l_list=np.linspace(0,L_b,N)


def Omega(theta,phi,N):
    
    d_theta=theta/N
    
    theta_list=np.linspace(0,theta,N)
    
    Integrand=phi*d_theta*np.sin(theta_list)
    
    return np.sum(Integrand)
    
def dR(l,w):
    
    delta_1_l=(L_b-L_t)/2 - Delta_L 
    delta_2_l=(L_b-L_t)/2 + Delta_L 
    
    delta_1_w=(W_b-W_t)/2 - Delta_W
    delta_2_w=(W_b-W_t)/2 + Delta_W 
    
    
    alpha_l=np.arctan((l-delta_1_l)/h)
    beta_l=np.arctan((L_b-l-delta_2_l)/h)
    
    alpha_w=np.arctan((w-delta_1_w)/h)
    beta_w=np.arctan((W_b-w-delta_2_w)/h)
    
    theta=alpha_w+beta_w
    phi=alpha_l+beta_l
    
    return Omega(theta,phi,1000)*dw_b*dl_b*flux


R=0

R_matrix=np.zeros((N,N))

for i,w in enumerate(w_list): #double integral
    for j,l in enumerate(l_list):
        R+=dR(l,w)
        R_matrix[i,j]=dR(l,w)
        
        
print(np.max(R_matrix/(flux*dw_b*dl_b)))
print(R)


plt.figure()
plt.imshow(R_matrix) # sanity-check



