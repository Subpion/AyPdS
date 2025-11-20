
import numpy as np
from scipy import signal as sig

import matplotlib.pyplot as plt
   
import scipy.io as sio
from scipy.io.wavfile import write
import sounddevice as sd


ecg_one_lead = np.load('ecg_sin_ruido.npy')

fs_ecg = 1000 # Hz

mat_struct = sio.loadmat('./ECG_TP4.mat')
ecg_ruido = mat_struct['ecg_lead'].flatten()


# plt.figure(1)
# plt.plot(ecg_ruido)
# plt.xlabel("eje de muestras discretas")
# plt.ylabel("eje de x[n]")
# plt.title("electro cardiograma")

#--------------------------ecg con ruido----------------------------
promedios=10 #10
zero_padding=2 #2
nperseg=ecg_ruido.shape[0]//promedios

f_welch , dsp_welch=sig.welch(x=ecg_ruido, fs=fs_ecg ,window="hamming",nperseg = nperseg, nfft=zero_padding*nperseg)

plt.figure(2)
plt.plot(f_welch,dsp_welch)
plt.xlabel("eje de frecuencias discretas")
plt.ylabel("eje de densidad espectral de potencia")
plt.title("ecg con ruido")
plt.legend()
plt.xlim(-0.1,50)
plt.ylim(0,1*10**7)
#--------------------------ecg sin ruido----------------------------
promedios=10 #10
zero_padding=2 #2
nperseg=ecg_one_lead.shape[0]//promedios

f_welch , dsp_welch=sig.welch(x=ecg_one_lead, fs=fs_ecg ,window="hamming",nperseg = nperseg, nfft=zero_padding*nperseg)

plt.figure(3)
plt.plot(f_welch,dsp_welch)
plt.xlabel("eje de frecuencias discretas")
plt.ylabel("eje de densidad espectral de potencia")
plt.title("ecg sin ruido")
plt.legend()
plt.xlim(-0.1,50)

plt.show()


