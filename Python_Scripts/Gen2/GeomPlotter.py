import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.close("all")

fig = plt.figure()

ax = fig.add_subplot(projection='3d')

R=100
N=100
Fact=1

ax.view_init(elev=80,azim=0)
ax.set_box_aspect((1,1,1))
ax.set_axis_off()

ax.set_xlim3d(-Fact*R,Fact*R)
ax.set_ylim3d(-Fact*R,Fact*R)
ax.set_zlim3d(-Fact*R,Fact*R)

def PlotSphereSurf(theta,phi,Origin,roty=0,rotx=0,initRot=False,a=1,R=1,c='b'):

    M0=np.array([1,0,0])    
    M=M0.copy()
    
    u=np.linspace(phi[0],phi[1],N)
    v=np.linspace(theta[0],theta[1],N)
    
    #'draw' the part of the sphere we want
    x0=R*np.outer(np.cos(u),np.sin(v))
    y0=R*np.outer(np.sin(u),np.sin(v))
    z0=R*np.outer(np.ones(N),np.cos(v))
    #Do y rotation:
    if initRot:
        x=-z0
        y=y0
        z=x0
        M[0]=-M0[2]
        M[1]=M0[1]
        M[2]=M0[0]
    else:
        x=x0
        y=y0
        z=z0
        M=M0
    #Do x rotation
    x0=x.copy()
    y0=y.copy()
    z0=z.copy()
    M0=M.copy()
    
    x=x0
    y=y0*np.cos(rotx)-z0*np.sin(rotx)
    z=z0*np.cos(rotx)+y0*np.sin(rotx)
    
    M=np.zeros(3)
    M[0]=M0[0]
    M[1]=M0[1]*np.cos(rotx)-M0[2]*np.sin(rotx)
    M[2]=M0[2]*np.cos(rotx)+M0[1]*np.sin(rotx)
    
    MNorm=-np.cross(M, [1,0,0]) #Vector to do second rotation around
    
    #Do y rotation
    x0=x.copy()
    y0=y.copy()
    z0=z.copy()
    
    
    for i in range(N):
        for j in range(N): #Run over all indices
            
    
            V=np.array([x0[i,j],y0[i,j],z0[i,j]])
            V0=V.copy()
            
            V=V0*np.cos(roty)+np.sin(roty)*np.cross(MNorm,V0)+(1-np.cos(roty))*np.dot(MNorm,V0)*MNorm
            
            #Add offset:
            V=V+Origin
            
            x[i,j]=V[0]
            y[i,j]=V[1]
            z[i,j]=V[2]
            
            
    ax.plot_surface(x,y,z,color=c,alpha=a)
    
    return M,MNorm

def PlotLine(Angle1,Angle2,Origin=[0,0,0]):
    
    r=np.linspace(0,R*Fact,N)
    
    x=r*np.cos(Angle1)*np.sin(Angle2)+Origin[0]
    y=r*np.sin(Angle1)*np.sin(Angle2)+Origin[1]
    z=r*np.cos(Angle2)+Origin[2]
    
    
    ax.plot(x,y,z,color='r')
    

def PlotLineVect(Vect,Origin=[0,0,0],scale=1,c='r'):

    Vect_Norm=np.array(Vect)/np.sqrt(np.dot(np.array(Vect),np.array(Vect)))

    r=np.linspace(0,scale,N)
    
    x=r*Vect_Norm[0]+Origin[0]
    y=r*Vect_Norm[1]+Origin[1]
    z=r*Vect_Norm[2]+Origin[2]
    
    
    ax.plot(x,y,z,color=c)

def PlotPLane(O,Norm,scale_x=1/N,scale_y=1/N,c='g',a=0.2):
    
    xx,yy=np.meshgrid(range(N),range(N))
    xx=xx*scale_x
    yy=yy*scale_y
    z=-(Norm[0]*xx+Norm[1]*yy-np.dot(O,Norm))/Norm[2]

    ax.plot_surface(xx,yy,z,color=c,alpha=a)
    
def PlotPLane2(xrange,yrange,height,c='g',a=0.2):
    
    xx,yy=np.meshgrid(np.linspace(xrange[0],xrange[1],N),np.linspace(yrange[0],yrange[1],N))
    xx=xx
    yy=yy
    z=height+xx*0

    ax.plot_surface(xx,yy,z,color=c,alpha=a)

def ROTX(V,a):
    W=V.copy()
    W[0]=V[0]
    W[1]=V[1]*np.cos(a)-np.sin(a)*V[2]
    W[2]=V[2]*np.cos(a)+np.sin(a)*V[1]
    return W
    
def ROTY(V,a):
    W=V.copy()
    W[0]=V[0]*np.cos(a)+V[2]*np.sin(a)
    W[1]=V[1]
    W[2]=V[2]*np.cos(a)-np.sin(a)*V[0]
    return W

def Findconer(sign,W_b,W_t,L_b,L_t,D_L,D_W,h):
    x=(W_b-W_t)/2 + sign[0] * W_t
    y=(L_b-L_t)/2+D_L + sign[1] * L_t
    z=h
    return np.array([x,y,z])

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

def FindAngle(A,B):
    A=np.array(A)
    B=np.array(B)
    return np.arccos(np.dot(A,B)/(np.sqrt(np.dot(A,A))*np.sqrt(np.dot(B,B))))
    

def Project(V,plane):
    if plane=="xy":
        return V*[1,1,0]
    if plane=="xz":
        return V*[1,0,1]
    if plane=="yz":
        return V*[0,1,1]
    return V
        

h=14.5

W_t=30
W_b=40

L_t=50
L_b=101

D_W=0
D_L=19-np.abs((L_t-L_b))/2


l=19
w=10

Origin=np.array([w,l,0])

Vectors=[]

"""
for i in range(2):
    for j in range(2):
        Corner=Findconer([i,j], W_b, W_t, L_b, L_t, D_L, D_W, h)
        V=Corner-Origin
        V=V/(np.sqrt(np.dot(V,V)))
        Vectors.append(V)
"""
for i in range(2):
    for j in range(2):
        PlaneMid=FindPlaneMid([i,j], W_b, W_t, L_b, L_t, D_L, D_W, h)
        V=PlaneMid-Origin
        V=V/(np.sqrt(np.dot(V,V)))
        Vectors.append(V)


Vectors=np.array(Vectors)

#print(Vectors)

eX=[1,0,0]
eY=[0,1,0]
eZ=[0,0,1]

Angles=[[],[]]

for v in Vectors:
    Angles[0].append(FindAngle(eZ,v))
    Angles[1].append(FindAngle(eX,v))

#MidVector=np.sum(Vectors,axis=0)
#MidVector=MidVector/(np.sqrt(np.dot(MidVector,MidVector)))
#print(MidVector)

#Angles[0].append(FindAngle(eZ,MidVector))
#Angles[1].append(FindAngle(eX,MidVector))

Angles=np.array(Angles)

#print(Angles)
"""
A=(Vectors[0]-MidVector)*np.array([1,1,0])
B=(Vectors[1]-MidVector)*np.array([1,1,0])
C=(Vectors[2]-MidVector)*np.array([1,1,0])
D=(Vectors[3]-MidVector)*np.array([1,1,0])

A=A/np.sqrt(np.dot(A,A))
B=B/np.sqrt(np.dot(B,B))
C=C/np.sqrt(np.dot(C,C))
D=D/np.sqrt(np.dot(D,D))

psi=FindAngle(A, B)#%(np.pi/2)
ksi=FindAngle(A, C)#%(np.pi/2)
psi2=FindAngle(D, B)
ksi2=FindAngle(D, C)
print(psi+ksi+psi2+ksi2)
"""


#Plot Bottom Detector:
PlotPLane2([0,W_b],[0,L_b],0)

#Plot Top Detector:
PlotPLane2([0+(W_b-W_t)/2,W_t+(W_b-W_t)/2],[0+(L_b-L_t)/2+D_L,L_t+(L_b-L_t)/2+D_L],h,c='orange')

 
LineLen=120

"""
#x,y,z axes:
PlotLineVect(eZ,c='b')
PlotLineVect(eY,c='g')
PlotLineVect(eX,c='r')
"""


s=0.8
Radius=LineLen*s

delta_1_l=(L_b-L_t)/2 - D_L 
delta_2_l=(L_b-L_t)/2 + D_L 

delta_1_w=(W_b-W_t)/2 - D_W
delta_2_w=(W_b-W_t)/2 + D_W 

if ((((l-delta_1_l)>=0) and ((L_b-delta_2_l-l)>=0)) and ((w-delta_1_w)>=0) and ((W_b-delta_2_w-w)>=0)): #we are below the top detector
    print("Below")
phi=FindAngle(Project(Vectors[0],plane="yz"),Project(Vectors[1],plane="yz"))
theta=FindAngle(Project(Vectors[3],plane="none"),Project(Vectors[2],plane="none"))

rotx=-(FindAngle(Project(Vectors[1],plane="yz"),eZ)+FindAngle(Project(Vectors[0],plane="yz"),eZ))/2#-(beta_l+alpha_l)

M0=np.array([1,0,0])    
M=M0.copy()
M[0]=-M0[2]
M[1]=M0[1]
M[2]=M0[0]
M0=M
M=np.zeros(3)
M[0]=M0[0]
M[1]=M0[1]*np.cos(rotx)-M0[2]*np.sin(rotx)
M[2]=M0[2]*np.cos(rotx)+M0[1]*np.sin(rotx)

MNorm=-np.cross(M, [1,0,0]) #Vector to do second rotation around

V2Proj=Vectors[2]-np.dot(Vectors[2],MNorm)*MNorm
V3Proj=Vectors[3]-np.dot(Vectors[2],MNorm)*MNorm

#PlotLineVect(V2Proj,Origin,scale=LineLen,c='k')
#PlotLineVect(V3Proj,Origin,scale=LineLen,c='k')

roty=(FindAngle(V2Proj,M)-FindAngle(V3Proj,M))/2#(beta_w-alpha_w)/2

M1,M2=PlotSphereSurf([np.pi/2-theta/2,np.pi/2+theta/2],[-phi/2,phi/2],Origin,rotx=rotx,roty=roty,a=0.4,R=Radius,initRot=True)

#PlotLineVect(M,Origin,scale=LineLen,c='cyan')
#PlotLineVect(MNorm,Origin,scale=LineLen,c='magenta')        

#Colors=['r','g','b','orange']
Colors=['r','r','r','r']

for v,c in zip(Vectors,Colors):
    PlotLineVect(v,Origin,scale=LineLen,c=c)

Vectors=[]

for i in range(2):
    for j in range(2):
        Corner=Findconer([i,j], W_b, W_t, L_b, L_t, D_L, D_W, h)
        V=Corner-Origin
        V=V/(np.sqrt(np.dot(V,V)))
        Vectors.append(V)

Colors=['k','k','k','k']

for v,c in zip(Vectors,Colors):
    PlotLineVect(v,Origin,scale=LineLen,c=c)

#PlotLineVect(MidVector,Origin,scale=LineLen,c='k')
#PlotLineVect(A,Origin,scale=LineLen,c='k')
#PlotLineVect(C,Origin,scale=LineLen,c='k')

"""
#Angle1=phi/2
#Angle2=np.pi/2+theta/2
#PlotLine(Angle1,Angle2)
#Corner=np.array([R*np.cos(Angle1)*np.sin(Angle2),R*np.sin(Angle1)*np.sin(Angle2),R*np.cos(Angle2)])
#Corner=np.array([-R*np.cos(Angle2),R*np.sin(Angle1)*np.sin(Angle2),R*np.cos(Angle1)*np.sin(Angle2)])
#Corner=np.array([-R*np.cos(Angle2)-Origin[2],R*np.sin(Angle1)*np.sin(Angle2)+Origin[1],R*np.cos(Angle1)*np.sin(Angle2)+Origin[0]])
#Corner=ROTX(Corner,rotx)
#Corner=ROTY(Corner,roty)
#Corner=Findconer([0,0], W_b, W_t, L_b, L_t, D_L, D_W, h)
#V=Corner-Origin
#PlotLineVect(V,Origin,scale=120)


Angle1=-phi/2
Angle2=np.pi/2+theta/2
Corner=np.array([-R*np.cos(Angle2)-Origin[2],R*np.sin(Angle1)*np.sin(Angle2)+Origin[1],R*np.cos(Angle1)*np.sin(Angle2)+Origin[0]])
Corner=ROTX(Corner,rotx)
Corner=ROTY(Corner,roty)
V=Corner-Origin
PlotLineVect(V,Origin,scale=120)

Angle1=phi/2
Angle2=np.pi/2-theta/2
Corner=np.array([-R*np.cos(Angle2)-Origin[2],R*np.sin(Angle1)*np.sin(Angle2)+Origin[1],R*np.cos(Angle1)*np.sin(Angle2)+Origin[0]])
Corner=ROTX(Corner,rotx)
Corner=ROTY(Corner,roty)
V=Corner-Origin
PlotLineVect(V,Origin,scale=120)

Angle1=-phi/2
Angle2=np.pi/2-theta/2
Corner=np.array([-R*np.cos(Angle2)-Origin[2],R*np.sin(Angle1)*np.sin(Angle2)+Origin[1],R*np.cos(Angle1)*np.sin(Angle2)+Origin[0]])
Corner=ROTX(Corner,rotx)
Corner=ROTY(Corner,roty)
V=Corner-Origin
PlotLineVect(V,Origin,scale=120)
"""

