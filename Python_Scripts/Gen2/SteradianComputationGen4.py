import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

def Project(V,plane):
    if plane=="xy":
        return V*[1,1,0]
    if plane=="xz":
        return V*[1,0,1]
    if plane=="yz":
        return V*[0,1,1]
    return V


def FindAngle(A,B):
    A=np.array(A)
    B=np.array(B)
    return np.arccos(np.dot(A,B)/(np.sqrt(np.dot(A,A))*np.sqrt(np.dot(B,B))))

def FindPlaneMid(sign,W_b,W_t,L_b,L_t,D_L,D_W,h):
    if sign == [0,0]:
        x=(W_b-W_t)/2+D_W + W_t/2 
        y=(L_b-L_t)/2+D_L
    if sign == [0,1]:
        x=(W_b-W_t)/2+D_W + W_t/2 
        y=(L_b-L_t)/2+D_L + L_t
    if sign == [1,0]:
        x=(W_b-W_t)/2+D_W
        y=(L_b-L_t)/2+D_L + L_t/2
    if sign == [1,1]:
        x=(W_b-W_t)/2+D_W + W_t
        y=(L_b-L_t)/2+D_L + L_t/2

    z=h
    return np.array([x,y,z])


#all in cm, s and sr

flux=6.64e-3

#from top to bottom
L=[50,101,80,100,101]
W=[30,40,38,40,40.5]
DL=[19,-5,7,-4,0]
H=[14.5,9.5,30,15.5]

Delta_W=0

plotcomb=[0,1]

Efficiency=0.85

N=100

GeomFactList=[]

DetectorLookup=[5,1,2,3,4]

#Run through all combinations:
for i in range(len(L)):
    for j in range(len(L)):
        if i<j: #j is bottom
            #print(i,j)
            print("Corresponding to Top: "+str(DetectorLookup[i])+" And bottom: "+str(DetectorLookup[j]))
            W_b=W[j]
            L_b=L[j]
            
            W_t=W[i]
            L_t=L[i]
            
            h=np.sum(H[i:j])
            
            D_L=np.sum(DL[i:j])-np.abs((L_t-L_b))/2
            D_W=0
            #print(h)
            #print(Delta_L)


            dw_b=W_b/N
            dl_b=L_b/N
            
            w_list=np.linspace(0,W_b,N)
            l_list=np.linspace(0,L_b,N)
            
            
            def Omega(theta,phi,N):
                
                d_theta=theta/N
                
                theta_list=np.linspace(np.pi*0.5-theta*0.5,np.pi*0.5+theta*0.5,N)
                
                Integrand=phi*d_theta*np.sin(theta_list)
                
                return np.sum(Integrand)
                
            def dR(l,w):
                
                Origin=np.array([w,l,0])
                
                Vectors=[]
                
                for i in range(2): #generate the 4 vectors to the sides
                    for j in range(2):
                        PlaneMid=FindPlaneMid([i,j], W_b, W_t, L_b, L_t, D_L, D_W, h)
                        V=PlaneMid-Origin
                        V=V/(np.sqrt(np.dot(V,V)))
                        Vectors.append(V)
                Vectors=np.array(Vectors)
                
                
                phi=FindAngle(Project(Vectors[0],plane="yz"),Project(Vectors[1],plane="yz"))
                theta=FindAngle(Project(Vectors[3],plane="none"),Project(Vectors[2],plane="none"))

                
                return Omega(theta,phi,1000)*dw_b*dl_b*flux
            
            
            R=0
            
            R_matrix=np.zeros((N,N))
            
            for I,w in enumerate(w_list): #double integral
                for J,l in enumerate(l_list):
                    R+=dR(l,w)
                    R_matrix[I,J]=dR(l,w)
                    
                    
            #print(np.max(R_matrix/(flux*dw_b*dl_b)))
            print("Rate assuming two detectors:"+str(R*Efficiency**2))
            print("Geom. Factor: "+str(R/(flux*L_b*W_b)))
            
            GeomFactList.append(R/(flux*L_b*W_b))
            
            if [i,j]==plotcomb:
                plt.figure()
                plt.imshow(R_matrix,interpolation='none',extent=[0,L_b,W_b,0]) # sanity-check
            
            
            
