import numpy as np
from scipy import signal
from scipy.fft import fft, fftshift
import matplotlib.pyplot as plt

N=1000
fs=N
deltaf=fs/N
a_0=2
snr_db=3

   
hamming = signal.windows.hamming(N)


flatop = signal.windows.flattop(N)

blackmanharris = signal.windows.blackmanharris(N)



fr=np.random.uniform(-2,2,N)



omega_0=fs/4 
omega_1=(omega_0+fr)*deltaf

potencia_señal=((a_0)**2)/2

dev_estandar=np.sqrt((potencia_señal)/(10**(snr_db/10)))


ruido=np.random.normal(0,dev_estandar ,(N))


t=np.arange(0,(N)/fs,1/fs)


s_1=a_0*np.sin(omega_1*2*np.pi*t)

x_1=s_1+ruido



ffx_1=(1/N)*np.fft.fft(x_1)
absffx_1=np.abs(ffx_1)
ff=np.arange(N)*(fs/(N))

ffx_2=(1/N)*np.fft.fft(x_1*hamming)
absffx_1=np.abs(ffx_1)
ff=np.arange(N)*(fs/(N))

ffx_3=(1/N)*np.fft.fft(x_1*flatop)
absffx_1=np.abs(ffx_1)
ff=np.arange(N)*(fs/(N))

ffx_4=(1/N)*np.fft.fft(x_1*blackmanharris)
absffx_1=np.abs(ffx_1)
ff=np.arange(N)*(fs/(N))

plt.figure(1)
plt.subplot(2,2,1)
plt.plot( np.abs(ffx_1), label="rectangular",linestyle='-',marker='' ,color='k')
plt.legend()
plt.xlim(200,300)
plt.ylabel("energia")
plt.xlabel("frecuencia normalizada")

plt.subplot(2,2,2)
plt.plot( np.abs(ffx_2), label="hamming",linestyle='-',marker='' ,color='g')
plt.legend()
plt.xlim(200,300)
plt.ylabel("energia")
plt.xlabel("frecuencia normalizada")

plt.subplot(2,2,3)
plt.plot( np.abs(ffx_3), label="flatop",linestyle='-',marker='' ,color='r')
plt.legend()
plt.xlim(200,300)
plt.ylabel("energia")
plt.xlabel("frecuencia normalizada")

plt.subplot(2,2,4)
plt.plot( np.abs(ffx_4), label="blackman harris",linestyle='-',marker='' ,color='b')
plt.legend()
plt.xlim(200,300)
plt.ylabel("energia")
plt.xlabel("frecuencia normalizada")



aux=np.sin(250*2*np.pi*t)

plt.figure(2)
plt.subplot(2,2,1)
plt.plot( np.arange(10*N)*(fs/(10*N)),10*np.log10(np.abs(np.fft.fft(aux,n=10*N))), label="rectangular",linestyle='-',marker='' ,color='k')
plt.legend()
plt.xlim(200,300)

plt.subplot(2,2,2)
plt.plot(np.arange(10*N)*(fs/(10*N)),10*np.log10(np.abs(np.fft.fft(aux*hamming,n=10*N))), label="hamming",linestyle='-',marker='' ,color='g')
plt.legend()
plt.xlim(200,300)

plt.subplot(2,2,3)
plt.plot(np.arange(10*N)*(fs/(10*N)),10*np.log10(np.abs(np.fft.fft(aux*flatop,n=10*N))), label="flatop",linestyle='-',marker='' ,color='r')
plt.legend()
plt.xlim(200,300)

plt.subplot(2,2,4)
plt.plot(np.arange(10*N)*(fs/(10*N)),10*np.log10(np.abs(np.fft.fft(aux*blackmanharris,n=10*N))), label="blackman harris",linestyle='-',marker='' ,color='b')
plt.legend()
plt.xlim(200,300)
plt.ylabel("db normalizada")
plt.xlabel("frecuencia normalizada")

