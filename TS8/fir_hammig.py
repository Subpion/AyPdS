import numpy as np
from scipy import signal as sig
import matplotlib.pyplot as plt
from scipy import signal
import scipy.io as sio
from scipy.io.wavfile import write
import sounddevice as sd
#------------------------señal------------------------
mat_struct = sio.loadmat('./ECG_TP4.mat')
ecg_one_lead = mat_struct['ecg_lead'].flatten()

ecg = np.load('ecg_sin_ruido.npy')
fs_ecg = 1000 # Hz

#--------plantilla de diseno-----------

wp= [0.8, 30]#frecuancia de corte/paso hz
ws= [0.1 , 30.7]  #frecuencia de stop/detenida hz



fs= 1000
frecuencias=np.sort(np.concatenate(((0,fs/2),wp,ws)))
deseado = [0,0,1,1,0,0]

cant_coef = 2000

retardo = (cant_coef -1)

#------diseno de filtro FIR------
fir_win_rec=sig.firwin2(numtaps=cant_coef,freq=frecuencias,gain=deseado,fs=fs,window="hamming")

#devuelve la respeuesta al impulso del filtro

w , h= sig.freqz(b= fir_win_rec,worN=np.logspace(-2,2,1000),fs=fs)

phase = np.unwrap(np.angle(h))
# Retardo de grupo = -dφ/dω
w_rad=w/(fs/2) *np.pi

gd = -np.diff(phase) / np.diff(w_rad)

# --- Polos y ceros ---
# z, p, k = signal.fir2zpk(sig.tf2sos(b=fir_win_hamming,a=1))


plt.figure(figsize=(12,10))

# Magnitud
plt.subplot(2,2,1)
plt.plot(w, 20*np.log10(abs(h)))
plt.title('Respuesta en Magnitud')
plt.xlabel('frecuencia [1/s]')
plt.ylabel('|H(jω)| [dB]')
plt.grid(True, which='both', ls=':')

# Fase
plt.subplot(2,2,2)
plt.plot(w, np.degrees(phase))
plt.title('Fase')
plt.xlabel('frecuencia [1/s]')
plt.ylabel('Fase [°]')
plt.grid(True, which='both', ls=':')

# Retardo de grupo
plt.subplot(2,2,3)
plt.plot(w[:-1], gd)
plt.title('Retardo de Grupo')
plt.xlabel('Pulsación angular [r/s]')
plt.ylabel('τg [s]')
plt.grid(True, which='both', ls=':')

# Diagrama de polos y ceros
# plt.subplot(2,2,4)
# plt.plot(np.real(p), np.imag(p), 'x', markersize=10, label='Polos')
# if len(z) > 0:
#                    plt.plot(np.real(z), np.imag(z), 'o', markersize=10, fillstyle='none', label='Ceros')
# plt.axhline(0, color='k', lw=0.5)
# plt.axvline(0, color='k', lw=0.5)
# plt.title('Diagrama de Polos y Ceros (plano s)')
# plt.xlabel('σ [rad/s]')
# plt.ylabel('jω [rad/s]')
# plt.legend()
# plt.grid(True)

# plt.tight_layout()
# plt.show()

ecg_filt_fir = sig.lfilter(b=fir_win_rec, a=1, x=ecg_one_lead)

plt.figure(2)
plt.plot(ecg_filt_fir,label = "FIR")#acordate de sacarle la demor por eso se ve feo
plt.plot(ecg_one_lead,label="original")
plt.legend()
#hacer filtrado de  cuadrados minimos