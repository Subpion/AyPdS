
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig


def mi_funcion_sen(vmax, dc, ff, ph, nn, fs):
    
    n = np.arange(0,nn)
    tt = n/fs
    w0 = 2 * np.pi * ff
    xx = dc + vmax * np.sin(w0 * tt + ph)
    
    return tt, xx


#%%
#N= 1000
#   fs1 = 1000  #resolucion espectral de 10 Hz
  #    vmax1=1
  #    dc1=0
 #     f1=1
 #     ph1=0
  #    t1,x1 = mi_funcion_sen(vmax=vmax1,dc=dc1,ff=f1,ph=ph1,nn=N,fs=fs1)

#  z = np.zeros(N, dtype=np.complex128())
#  for k in range(N):
#      for n in range(N):
#       z[k] += x1[n] * np.exp(-1j * k * np.pi * 2 * n / N)
       
#   
#%%
        
#N=8
#x=np.zeros(N)
#y=np.zeros(N)
#y[5]=1
#x[:2]=1
#rxx=sig.correlate(x,y)
#rxy = sig.convolve(x,y)
#plt.figure(1)
#plt.clf()
#plt.plot(x,'x:',label='x')
#plt.plot(y,'y:',label='y')    
#plt.plot( rxx,'o:',label='con')
#plt.plot( rxy,'o:',label='con')


plt.show()
#%%
N=8
n=  np.arange(N)
x=4 + 3*np.sin(np.pi*n/2)
M=4
m=np.arange(M )
y=x[-m]
z=np.arange(N)
#DFT
for k in range(N):
    for n in range(N):
        z[k] += x[n] * np.exp(-1j * k * np.pi * 2 * n / N)
       

