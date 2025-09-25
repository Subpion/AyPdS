import numpy as np
from scipy import signal
from scipy.fft import fft, fftshift
import matplotlib.pyplot as plt

N=1000
fs=N
deltaf=fs/N
a_0=2
snr_db=3
realizaciones=200
   
hamming = signal.windows.hamming(N)
hamming = np.reshape(hamming,(N,1))

flatop = signal.windows.flattop(N)
flatop= np.reshape(flatop,(N,1))

blackmanharris = signal.windows.blackmanharris(N)
blackmanharris= np.reshape(blackmanharris,(N,1))

fr=np.random.uniform(-2,2,(N,realizaciones))


# fr=np.random.uniform(-2,2,(realizaciones))
# fr=np.reshape(fr,(1,realizaciones))
# fr=np.tile(fr, (N,1))


omega_0=fs/4 
omega_1=(omega_0+fr)*deltaf

potencia_señal=((a_0)**2)/2

dev_estandar=np.sqrt((potencia_señal)/(10**(snr_db/10)))


ruido=np.random.normal(0,dev_estandar ,(N,realizaciones))


t=np.arange(0,(N)/fs,1/fs)
t=np.reshape(t,(N,1))
t=np.tile(t, (1,realizaciones))

s_1=a_0*np.sin(omega_1*2*np.pi*t)

x_1=s_1+ruido




ffx_1=(1/(N))*np.fft.fft(x_1,n=N,axis=0)
absffx_1=np.abs(ffx_1)
ff=np.arange(N)*(fs/(N))

ffx_2=(1/(N))*np.fft.fft(x_1*hamming,n=N,axis=0)
absffx_1=np.abs(ffx_1)
ff=np.arange(N)*(fs/(N))

ffx_3=(1/(N))*np.fft.fft(x_1*flatop,n=N,axis=0)
absffx_1=np.abs(ffx_1)
ff=np.arange(N)*(fs/(N))

ffx_4=(1/(N))*np.fft.fft(x_1*blackmanharris,n=N,axis=0)
absffx_1=np.abs(ffx_1)
ff=np.arange(N)*(fs/(N))


estimador_1=np.argmax(np.abs(ffx_1[0:500:]),axis=0)
var_rectangular=np.var(estimador_1)
media_rectangular=np.mean(estimador_1)


estimador_2=np.argmax(np.abs(ffx_2[0:500,:]),axis=0)
var_hamming=np.var(estimador_2)
media_hamming=np.mean(estimador_2)


estimador_3=np.argmax(np.abs(ffx_3[0:500,:]),axis=0)
var_flatop=np.var(estimador_3)
media_flatop=np.mean(estimador_3)


estimador_4=np.argmax(np.abs(ffx_4[0:500,:]),axis=0)
var_bcharris=np.var(estimador_4)
media_bcharrix=np.mean(estimador_4)


claridad=0.4
bins=20

aux1=np.abs(ffx_4[0:500][:])
aux2=np.abs(ffx_4[0:500,:])

plt.clf
plt.figure(1)
plt.subplot(2,2,1)
plt.hist(estimador_1,bins,alpha=claridad,label="rectangular")
plt.legend()
plt.subplot(2,2,2)
plt.hist(estimador_2,bins,alpha=claridad,label="hamming")
plt.legend()
plt.subplot(2,2,3)
plt.hist(estimador_3,bins,alpha=claridad,label="flattop")
plt.legend()
plt.subplot(2,2,4)
plt.hist(estimador_4,bins,alpha=claridad,label="blackmanharris")
plt.legend()
plt.show()

print('               | media            |varianza              |')
print("rectangular    |",media_rectangular,"  |",var_rectangular," |",)
print("hamming        |",media_hamming,"  |",var_hamming," |",)
print("flattop        |",media_flatop,"  |",var_flatop,"|",)
print("blackman harris|",media_bcharrix," |",var_bcharris,"|",)