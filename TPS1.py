
import numpy as np
import matplotlib.pyplot as plt


def mi_funcion_sen(vmax, dc, ff, ph, nn, fs):
    
    n = np.arange(0,nn)
    tt = n/fs
    w0 = 2 * np.pi * ff
    xx = dc + vmax * np.sin(w0 * tt + ph)
    
    return tt, xx

def mi_funcion_mod(vmax, dc, ff, ph, nn, fs):
    
    n = np.arange(0,nn)
    tt = n/fs
    w0 = 2 * np.pi * ff
    xx = (dc + vmax * np.sin(w0 * tt + ph))*(dc + vmax * np.sin((w0/2) * tt +ph))
    
    return tt, xx

from scipy import signal
def mi_funcion_cuad(vmax=1, dc=0, ff=1, ph=0, nn=1000, fs=1000, duty=0.5):
    tt = np.arange(0,nn)/fs
    xx = signal.square(2 * np.pi * ff * tt + ph, duty=duty)
    xx = dc + (vmax * xx)
    # Asegurar forma Nx1
    tt = tt.reshape(-1,1)
    xx = xx.reshape(-1,1)
    
    return tt, xx

#%%
N = 200
fs1 = 40000  #resolucion espectral de 10 Hz
vmax1=1
dc1=0
f1=2000
ph1=0
t1,x1 = mi_funcion_sen(vmax=vmax1,dc=dc1,ff=f1,ph=ph1,nn=N,fs=fs1)

vmax2=2
dc2=0
f2=f1
ph2= np.pi / 2
t2,x2 = mi_funcion_sen(vmax=vmax2,dc=dc2,ff=f2,ph=ph2,nn=N,fs=fs1)

fig, axs = plt.subplots(2, 1)
axs[0].plot(t1, x1, color='blue')
axs[0].set_title('Senoidal 2KHz')
axs[0].set_xlabel('Tiempo [s]')
axs[0].set_ylabel('Amplitud [V]')
axs[0].grid(True)

# Plot on the second subplot
axs[1].plot(t2, x2, color='red')
axs[1].set_title('Senoidal amplificada y desfazada')
axs[1].set_xlabel('Tiempo [s]')
axs[1].set_ylabel('Amplitud [V]')
axs[1].grid(True)

ta,xa = mi_funcion_sen(vmax=vmax1,dc=dc1,ff=f1/2,ph=ph1,nn=N,fs=fs1)
t3,x3 = mi_funcion_mod(vmax=vmax1,dc=dc1,ff=f1,ph=ph1,nn=N,fs=fs1)

fig, ax = plt.subplots(2, 1)
ax[0].plot(t1, x1, color='blue')
ax[0].plot(ta,xa,color='red')
ax[0].set_title('Senoidales con frecuencia 2KHz y 1KHz')
ax[0].set_xlabel('Tiempo [s]')
ax[0].set_ylabel('Amplitud [V]')
ax[0].grid(True)

# Plot on the second subplot
ax[1].plot(t3, x3, color='red')
ax[1].set_title('Señal modulada')
ax[1].set_xlabel('Tiempo [s]')
ax[1].set_ylabel('Amplitud [V]')
ax[1].grid(True)

threshold= 0.75 * (vmax1**2)/2
x4 = np.clip(x1,-threshold,threshold)
plt.figure(6)
plt.plot(t1,x4)
plt.title('Señal recortada al 75% de la potencia')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud [V]')
plt.grid(True)
plt.show()

t5,x5 = mi_funcion_cuad(vmax=vmax1,dc=dc1,ff=4000,ph=ph1,nn=N,fs=fs1,duty=0.5)
plt.figure(7)
plt.plot(t5,x5)
plt.title('Señal cuadrada de 4KHz')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud [V]')
plt.grid(True)
plt.show()