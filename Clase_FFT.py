# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 18:55:38 2025

@author: vange
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft

def sen(ff, nn,vmax=1, dc=0, ph=0, fs=2):
    
    n = np.arange(0,nn)
    tt = n/fs
    w0 = 2 * np.pi * ff
    xx = dc + vmax * np.sin(w0 * tt + ph)
    
    return tt, xx
N = 1000
Fs = N
df = Fs/N
# %%



t1,x1 = sen(ff=(N/4)*df,nn=N,fs=Fs)
t2,x2 = sen(ff=(N/4 +1)*df,nn=N,fs=Fs)
t3,x3 = sen(ff=((N/4) + 0.5)*df,nn=N,fs=Fs)
plt.plot(t1, x1)
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud [V]")
plt.title("Señal senoidal")
plt.grid(True)
plt.show()


X1 = fft(x1)
X2 = fft(x2)
X3 = fft(x3)
X1ab = np.abs(X1)
X2ab = np.abs(X2)
X3ab = np.abs(X3)
X1ang = np.angle(X1)
X2ang = np.angle(X2)
X3ang = np.angle(X3)

X1dB=np.log10(X1ab)*20
X2dB=np.log10(X2ab)*20
X3dB=np.log10(X3ab)*20

frec= np.arange(N)*df

plt.plot(frec,X1dB,'x',label="Transformada en N/4")
plt.plot(frec,X2dB,'x',label="Transformada en N/4+1")
plt.plot(frec,X3dB,'x',label="Transformada en N/4+1/2")
plt.xlabel("Frecuencia")
plt.xlim(0,Fs/2)
plt.ylabel("dB")
plt.legend()
plt.title("FFT")
plt.grid(True)
plt.show()
# %%
v1=np.sqrt(2)
t1,x1=sen(ff=(N/4)*df,nn=N, vmax= v1,fs=Fs)
var= np.var(x1)
std = np.std(x1)
# xx2=np.abs(x1)**2 
# media =np.mean(xx2)
# xx1dB = np.log10(media)*10

x1dft= np.log10(np.abs(fft(x1)))

print(f"Varianza medida = {var:.5f}")
print(f"Desvio Estandar = {std:.5f}")
# print(f"|x|**2 = {xx1dB:.5f}")


frec= np.arange(N)*df

plt.plot(frec,x1dft,':x',label="Transformada en N/4")
plt.xlabel("Frecuencia")

plt.ylabel("dB")
plt.legend()
plt.title("FFT")
plt.grid(True)
plt.show()




#comprobar Peseval y Zero Paddling



























