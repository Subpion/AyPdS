import numpy as np
from scipy import signal
from scipy.fft import fft, fftshift
import matplotlib.pyplot as plt

N=1000
fs=N
deltaf=fs/N
a_0=np.sqrt(2)
snr_db=10
realizaciones=200
   
fr=np.random.uniform(-2,2,realizaciones)
fr=np.reshape(fr,(1,realizaciones))
fr=np.tile(fr, (N,1))


omega_0=fs/4 
omega_1=(omega_0+fr)*deltaf

potencia_señal=((a_0)**2)/2

dev_estandar=np.sqrt((potencia_señal)/(10**(snr_db/10)))


ruido=np.random.normal(0,dev_estandar ,N)
ruido=np.reshape(ruido,(N,1))
ruido=np.tile(ruido, (1,realizaciones))

t=np.arange(0,(N)/fs,1/fs)
t=np.reshape(t,(N,1))
t=np.tile(t, (1,realizaciones))

s_1=a_0*np.sin(omega_1*2*np.pi*t)

x_1=s_1+ruido


plt.figure(2)
plt.clf

ffx_1=(1/N)*np.fft.fft(x_1,n=10*N,axis=0)
absffx_1=np.abs(ffx_1)
ff=np.arange(N)*(fs/(N))

plt.plot(np.arange(10*N)(fs/(10*N)),10*np.log10(2(np.abs(ffx_1)**2)),linestyle='-',marker='.' )

plt.grid(True, linestyle=':') 
plt.xlabel('frecuencia (HZ)')
plt.ylabel('f(w)')
plt.xlim(0,N/2)
#plt.axis([0,nn/2,0,10000]
plt.draw()
plt.tight_layout() 

plt.show()