import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

Delta_t=40e-9

R2=0.18550095112426532 #From datafiles
R3=0.0893841375169187

p=np.array([1,-1,0,(R2-R3)*Delta_t])

x=np.linspace(-1,2,100)

plt.plot(x,p[0]*x**3+p[1]*x**2+p[2]*x+p[3])

roots=np.roots(p)

print("p = "+str(roots))
print("q = "+str(R2*Delta_t-roots**2))

q=(R2*Delta_t-roots[1]**2)

print(roots[1]**3/Delta_t)
print(q/Delta_t)
print((q+roots[1]**2)/Delta_t)
print(roots[1]**2/Delta_t)
