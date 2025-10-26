import numpy as np
from scipy import signal as sig

import matplotlib.pyplot as plt
   
import scipy.io as sio
from scipy.io.wavfile import write

ecg_one_lead = np.load('ecg_sin_ruido.npy')
fs_ecg = 1000 # Hz

plt.figure(1)
plt.plot(ecg_one_lead)
plt.xlabel("eje de muestras discretas")
plt.ylabel("eje de x[n]")
plt.title("electro cardiograma")

#--------------------------welch----------------------------
promedios=10#10
zero_padding=2
nperseg=ecg_one_lead.shape[0]//promedios

f_welch , dsp_welch=sig.welch(x=ecg_one_lead, fs=fs_ecg ,window="hamming",nperseg = nperseg, nfft=zero_padding*nperseg)

area=np.cumsum(dsp_welch)

bb_max=np.where((area/np.max(area))>0.99)
bw_max_welch=f_welch[bb_max[0][0]]

bb_min=np.where(dsp_welch>dsp_welch[bb_max[0][0]])
bw_min_welch=f_welch[bb_min[0][0]]

plt.figure(2)
plt.plot(f_welch,dsp_welch)
plt.xlabel("eje de frecuencias discretas")
plt.ylabel("eje de densidad espectral de potencia")
plt.title("welch")
plt.axvline(x=bw_max_welch,color='g',label="frecuencia maxima")
plt.axvline(x=bw_min_welch,color="r",label="frecuencia minima")
plt.legend()
plt.xlim(-0.1,50)
#----------------------periodograma modificado-------------
hamming = sig.windows.hamming(len(ecg_one_lead))

x_n=hamming*ecg_one_lead
dsp_perio=np.fft.fft(x_n)
dsp_perio=(np.abs(dsp_perio)**2)/len(ecg_one_lead)
dsp_perio=dsp_perio[0:int(len(dsp_perio)/2)]
f_perio=(fs_ecg/len(ecg_one_lead))*np.arange(len(dsp_perio))

area=np.cumsum(dsp_perio)

bb_max=np.where((area/np.max(area))>0.99)
bw_max_perio=f_perio[bb_max[0][0]]

bb_min=np.where(dsp_perio>dsp_perio[bb_max[0][0]])
bw_min_perio=f_perio[bb_min[0][0]]


plt.figure(3)
plt.plot(f_perio,dsp_perio)
plt.xlabel("eje de frecuencias discretas")
plt.ylabel("eje de densidad espectral de potencia")
plt.title("periodograma modificado")
plt.axvline(x=bw_max_perio,color='g',label="frecuencia maxima")
plt.axvline(x=bw_min_perio,color="r",label="frecuencia minima")
plt.legend()
plt.xlim(-0.1,50)
plt.ylim(0,2*10**9)

plt.show()
#por que en perio aparece frecuencias al final? por nyquist creo pq aparence espejadas
#--------------------------------------tabla de anchos de banda-------------------------------
print("     ancho de banda    |  inferior      |    superior")
print("periodograma modificado|",bw_min_perio,"|",bw_max_perio," |",)
print("welch                  |",bw_min_welch,"|",bw_max_welch," |",)


fs_ppg = 400 # Hz

ppg = np.load('ppg_sin_ruido.npy')

plt.figure(1)
plt.plot(ppg)

plt.xlabel("eje de muestras discretas")
plt.ylabel("eje de x[n]")
plt.title("plestimografia")
#--------------------------------------welch-----------------------------------
promedios=20#20
zero_padding=2
nperseg=ppg.shape[0]//promedios
f_welch_ppg , psd_welch_ppg = sig.welch(x=ppg, fs=fs_ppg ,window="hamming",nperseg = nperseg, nfft=zero_padding*nperseg)

area=np.cumsum(psd_welch_ppg)
bb_max=np.where((area/np.max(area))>0.99)
bw_max_welch=f_welch_ppg [bb_max[0][0]]
bb_min=np.where(psd_welch_ppg>psd_welch_ppg[bb_max[0][0]])
bw_min_welch=f_welch_ppg[bb_min[0][0]]


plt.figure(2)
plt.plot(f_welch_ppg,psd_welch_ppg)
plt.xlabel("eje de frecuencias discretas")
plt.ylabel("eje de densidad espectral de potencia")
plt.title("periodograma modificado")
plt.axvline(x=bw_max_welch,color='g',label="frecuencia maxima")
plt.axvline(x=bw_min_welch,color="r",label="frecuencia minima")
plt.legend()
plt.xlim(0,10)

#----------------------periodograma modificado-------------
#aclaracion: por se que lo tranformamos medio a mano las frecuencias se repite en nyquist por lo tanto 
#hay que cortar a la mitad la dessidad espectral de potencia(supongo)
hamming = sig.windows.hamming(len(ppg))

x_n=hamming*ppg
dsp_perio=np.fft.fft(x_n)
dsp_perio=(np.abs(dsp_perio)**2)/len(ppg)
dsp_perio=dsp_perio[0:int(len(dsp_perio)/2)]#lo hice a mano pq hacer len(wav_data) te lo convierte en flotante y eso no le gusta en vectores 
f_perio=(fs_ppg/len(ppg))*np.arange(len(dsp_perio))

area=np.cumsum(dsp_perio)

bb_max=np.where((area/np.max(area))>0.99)
bw_max_perio=f_perio[bb_max[0][0]]
bb_min=np.where(dsp_perio>dsp_perio[bb_max[0][0]])
bw_min_perio=f_perio[bb_min[0][0]]


plt.figure(3)
plt.plot(f_perio,dsp_perio)
plt.xlabel("eje de frecuencias discretas")
plt.ylabel("eje de densidad espectral de potencia")#que deberia poner?
plt.title("periodograma modificado")
plt.axvline(x=bw_max_perio,color='g',label="frecuencia maxima")
plt.axvline(x=bw_min_perio,color="r",label="frecuencia minima")
plt.legend()

plt.xlim(0,10)

plt.show()
#--------------------------------------tabla de anchos de banda-------------------------------
print("     ancho de banda    |  inferior      |    superior")
print("periodograma modificado|",bw_min_perio,"|",bw_max_perio," |",)
print("welch                  |",bw_min_welch,"|",bw_max_welch," |",)




fs_audio, wav_data = sio.wavfile.read('silbido.wav')

plt.figure(1)
plt.plot(wav_data)
plt.xlabel("eje de muestras discretas")
plt.ylabel("eje de x[n]")
plt.title("audio: silbido")
#---------------------------welch------------------------------------
promedios=40 #50
zero_padding=1
nperseg=wav_data.shape[0]//promedios

f_welch_ha , psd_welch_ha=sig.welch(x=wav_data, fs=fs_audio ,window="hamming",nperseg = nperseg, nfft=zero_padding*nperseg)

area=np.cumsum(psd_welch_ha)
bb_max=np.where((area/np.max(area))>0.99)
bw_max_welch=f_welch_ha[bb_max[0][0]]
bb_min=np.where(psd_welch_ha>psd_welch_ha[bb_max[0][0]])
bw_min_welch=f_welch_ha[bb_min[0][0]]

plt.figure(2)
plt.plot(f_welch_ha,psd_welch_ha)
plt.xlabel("eje de frecuencias discretas")
plt.ylabel("eje de densidad espectral de potencia")
plt.title("welch")
plt.axvline(x=bw_max_welch,color='g',label="frecuencia maxima")
plt.axvline(x=bw_min_welch,color="r",label="frecuencia minima")
plt.legend()
plt.xlim(0,10000)

#----------------------periodograma modificado-------------
#aclaracion: por se que lo tranformamos medio a mano las frecuencias se repite en nyquist por lo tanto 
#hay que cortar a la mitad la dessidad espectral de potencia
hamming = sig.windows.hamming(len(wav_data))

x_n=hamming*wav_data
dsp_perio=np.fft.fft(x_n)
dsp_perio=(np.abs(dsp_perio)**2)/len(wav_data)
dsp_perio=dsp_perio[0:72000]#lo hice a mano pq hacer len(wav_data) te lo convierte en flotante y eso no le gusta en vectores 
f_perio=(fs_audio/len(wav_data))*np.arange(len(dsp_perio))

area=np.cumsum(dsp_perio)

bb_max=np.where((area/np.max(area))>0.99)
bw_max_perio=f_perio[bb_max[0][0]]
bb_min=np.where(dsp_perio>dsp_perio[bb_max[0][0]])
bw_min_perio=f_perio[bb_min[0][3]]


plt.figure(3)
plt.plot(f_perio,dsp_perio)
plt.xlabel("eje de frecuencias discretas")
plt.ylabel("eje de densidad espectral de potencia")
plt.title("periodograma modificado")
plt.axvline(x=bw_max_perio,color='g',label="frecuencia maxima")
plt.axvline(x=bw_min_perio,color="r",label="frecuencia minima")
plt.legend()
plt.xlim(-0.1,10000)
plt.ylim(0,1*10**-1)
plt.show()
#por que la potencia no da igual?
#--------------------------------------tabla de anchos de banda-------------------------------
print("     ancho de banda    |  inferior      |    superior")
print("periodograma modificado|",bw_min_perio,"|",bw_max_perio," |",)
print("welch                  |",bw_min_welch,"|",bw_max_welch," |",)




