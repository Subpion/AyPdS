import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
def sen(ff, nn,vmax=1, dc=0, ph=0, fs=2):
    
    tt = np.arange(0,nn)/fs
    w0 = 2 * np.pi * ff
    xx = dc + vmax * np.sin(w0 * tt + ph)
    
    return tt, xx

def modu(fs, nn,vmax=1, dc=0, ph=0,ff=50 ):
    
    tt = np.arange(0,nn)/fs
    w0 = 2 * np.pi * ff
    xx = (dc + vmax * np.sin(w0 * tt + ph))*(dc + vmax * np.sin((w0/2) * tt +ph))
    
    return tt, xx


def cuad(fs, nn,vmax=1, dc=0, ph=0,ff=50 , duty=0.5):
    tt = np.arange(0,nn)/fs
    xx = dc + (vmax *sig.square(2 * np.pi * ff * tt + ph, duty=duty))

    
    return tt, xx

def cos(fs, nn,vmax=1, dc=0, ph=0,ff=50 ):

    tt = np.arange(0,nn)/fs
    w0 = 2 * np.pi * ff
    xx = dc + vmax * np.cos(w0*tt+ph)
    
    return tt, xx

# Una señal sinusoidal de 2KHz.
fs1=40000
N=800
f1=2000
t1,x1 = sen(nn=N,fs=fs1,ff=f1)
df=fs1/N
# Misma señal amplificada y desfazada en π/2.
v1=2
ph1=np.pi/2
_,x2 = sen(nn=N,fs=fs1,vmax=v1,ff=f1,ph=ph1)
# Misma señal modulada en amplitud por otra señal sinusoidal de la mitad de la frecuencia.
t3,x3 = modu(ff=f1,ph=ph1,nn=N,fs=fs1)
# Señal anterior recortada al 75% de su amplitud
threshold= 0.75 * (1**2)/2
x4 = np.clip(x1,-threshold,threshold)
# Una señal cuadrada de 4KHz.
f2=4000
t5,x5 = cuad(nn=N,fs=fs1,ff=f2,duty=0.5)
# Un pulso rectangular de 10ms.
f3=50
t6,x6=cuad(nn=N,fs=fs1,ff=f3,duty=0.5)


b=np.array([3*(10**(-2)), 5*(10**(-2)), 3*(10**(-2)) ])
a=np.array([1.0, -1.5, 0.5])
y1= sig.lfilter(b, a, x1)

fig, axs = plt.subplots(2, 1)
axs[0].plot(t1, x1, color='blue')
axs[0].set_title('Senoidal 2KHz')
axs[0].set_xlabel('Tiempo [s]')
axs[0].set_ylabel('Amplitud [V]')

axs[0].grid(True)

axs[1].plot(t1, y1, color='red')
axs[1].set_title('Salida')
axs[1].set_xlabel('Tiempo [s]')
axs[1].set_ylabel('Amplitud [V]')

axs[1].grid(True)

# y2= sig.lfilter(b, a, x2)

# fig, axs = plt.subplots(2, 1)
# axs[0].plot(t1, x2, color='blue')
# axs[0].set_title('Senoidal 2KHz, amplificada y desplazada ')
# axs[0].set_xlabel('Tiempo [s]')
# axs[0].set_ylabel('Amplitud [V]')
# axs[0].set_xlim(0, 0.0025)
# axs[0].grid(True)

# axs[1].plot(t1, y2, color='red')
# axs[1].set_title('Salida')
# axs[1].set_xlabel('Tiempo [s]')
# axs[1].set_ylabel('Amplitud [V]')
# axs[1].set_xlim(0, 0.0025)
# axs[1].grid(True)


# y3= sig.lfilter(b, a, x3)

# fig, axs = plt.subplots(2, 1)
# axs[0].plot(t3, x3, color='blue')
# axs[0].set_title('Senoidal Modulada')
# axs[0].set_xlabel('Tiempo [s]')
# axs[0].set_ylabel('Amplitud [V]')
# axs[0].set_xlim(0, 0.0025)
# axs[0].grid(True)

# axs[1].plot(t3, y3, color='red')
# axs[1].set_title('Salida')
# axs[1].set_xlabel('Tiempo [s]')
# axs[1].set_ylabel('Amplitud [V]')
# axs[1].set_xlim(0, 0.0025)
# axs[1].grid(True)

# y4= sig.lfilter(b, a, x4)

# fig, axs = plt.subplots(2, 1)
# axs[0].plot(t1, x4, color='blue')
# axs[0].set_title('Senoidal Recortada')
# axs[0].set_xlabel('Tiempo [s]')
# axs[0].set_ylabel('Amplitud [V]')
# axs[0].set_xlim(0, 0.0025)
# axs[0].grid(True)

# axs[1].plot(t1, y4, color='red')
# axs[1].set_title('Salida')
# axs[1].set_xlabel('Tiempo [s]')
# axs[1].set_ylabel('Amplitud [V]')
# axs[1].set_xlim(0, 0.0025)
# axs[1].grid(True)

# y5= sig.lfilter(b, a, x5)

# fig, axs = plt.subplots(2, 1)
# axs[0].plot(t5, x5, color='blue')
# axs[0].set_title('Señal cuadrada de 4KHz')
# axs[0].set_xlabel('Tiempo [s]')
# axs[0].set_ylabel('Amplitud [V]')
# axs[0].set_xlim(0, 0.0025)
# axs[0].grid(True)

# axs[1].plot(t5, y5, color='red')
# axs[1].set_title('Salida')
# axs[1].set_xlabel('Tiempo [s]')
# axs[1].set_ylabel('Amplitud [V]')
# axs[1].set_xlim(0, 0.0025)
# axs[1].set_ylim(0, 3)
# axs[1].grid(True)

# y6= sig.lfilter(b, a, x6)

# fig, axs = plt.subplots(2, 1)
# axs[0].plot(t6, x6, color='blue')
# axs[0].set_title('Pulso rectangular de 10ms')
# axs[0].set_xlabel('Tiempo [s]')
# axs[0].set_ylabel('Amplitud [V]')
# axs[0].grid(True)

# axs[1].plot(t6, y6, color='red')
# axs[1].set_title('Salida')
# axs[1].set_xlabel('Tiempo [s]')
# axs[1].set_ylabel('Amplitud [V]')
# axs[1].grid(True)


delta = np.zeros(N)
delta[0] = 1.0


h1 = sig.lfilter(b, a, delta)

Yx1h = np.convolve(x1, h1)
b=[3*(10**(-2)), 5*(10**(-2)), 3*(10**(-2)) ]
a=[1.0, -1.5, 0.5]
y1= sig.lfilter(b, a, x1)
# frec=np.arange(N)*df
plt.figure(2)
plt.plot(Yx1h)
plt.title('Salida de convolucion')
plt.xlabel('Muestras [N] ')
plt.ylabel('Amplitud [V]')
plt.grid(True)
plt.show()

f4=200

t7,x7= sen( fs=fs1, nn=N, ff= f4 )
c= np.zeros(11); c[0]=1; c[10]=3

d = np.array([1.0])

h2= sig.lfilter(c, d, x7)

Yx7h = np.convolve(x7, h2)



fig, axs = plt.subplots(2, 1)
axs[0].plot(t7, x7, color='blue')
axs[0].set_title('Senoidal de 500 Hz')
axs[0].set_xlabel('Tiempo [s]')
axs[0].set_ylabel('Amplitud [V]')
axs[0].grid(True)

axs[1].plot(Yx7h)
axs[1].set_title('Salida')
axs[1].set_xlabel('Tiempo [s]')
axs[1].set_ylabel('Amplitud [V]')

axs[1].grid(True)

e= np.array([1.0])


f = np.zeros(11); f[0]=1; f[10]=3

h3= sig.lfilter(e, f, x7)

Yx8h = np.convolve(x7, h3)



fig, axs = plt.subplots(2, 1)
axs[0].plot(t7, x7, color='blue')
axs[0].set_title('Senoidal de 500 Hz')
axs[0].set_xlabel('Tiempo [s]')
axs[0].set_ylabel('Amplitud [V]')
axs[0].grid(True)

axs[1].plot(Yx8h)
axs[1].set_title('Salida')
axs[1].set_xlabel('Tiempo [s]')
axs[1].set_ylabel('Amplitud [V]')

axs[1].grid(True)



