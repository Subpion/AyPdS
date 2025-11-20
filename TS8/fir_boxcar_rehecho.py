

import numpy as np
from scipy import signal as sig

import matplotlib.pyplot as plt
from scipy import signal
import scipy.io as sio
from scipy.io.wavfile import write
import sounddevice as sd



mat_struct = sio.loadmat('ECG_TP4.mat')
ecg_one_lead = mat_struct['ecg_lead'].flatten()
fs=1000
cant_muestras=ecg_one_lead.shape[0]


#############
# Plantilla #
#############

nyq_frec = fs/2
ripple = 1 # dB
atenuacion = 40 # dB
 
ws1 = 0.1 # Hz
wp1 = 0.8 # Hz
wp2 = 30 # Hz
ws2 = 30.7 # Hz
 
# plantilla normalizada a Nyquist en dB
frecs = np.array([0,         ws1,         wp1,     wp2,     ws2,         fs/2  ]) 
gains = np.array([-atenuacion, -atenuacion, -ripple, -ripple, -atenuacion, -atenuacion])
 
# convertimos a veces para las funciones de diseño
gains = 10**(gains/20)


gains[5]=0 

####################
# Diseño del filtro#
####################

cant_coef = 2000
demora = (cant_coef -1)

fir_win_rec=sig.firwin2(numtaps=cant_coef,freq=frecs,gain=gains,fs=fs,window="boxcar")


ECG_f_win = sig.lfilter(b=fir_win_rec, a=1, x=ecg_one_lead)

##########################
# respuesta en frecuencia#
##########################

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

plt.tight_layout()
plt.show()

###################################
# Regiones de interés con ruido #
###################################

regs_interes = (
        [4000, 5500], # muestras
        [10e3, 11e3], # muestras
        )
 
for ii in regs_interes:
   
    # intervalo limitado de 0 a cant_muestras
    zoom_region = np.arange(np.max([0, ii[0]]), np.min([cant_muestras, ii[1]]), dtype='uint')
   
    plt.figure()
    plt.plot(zoom_region, ecg_one_lead[zoom_region], label='ECG', linewidth=2)
    plt.plot(zoom_region, ECG_f_win[zoom_region + demora], label='FIR Window')
   
    plt.title('filtro fir ventana cuadrada con ecg de' + str(ii[0]) + ' a ' + str(ii[1]) )
    plt.ylabel('Adimensional')
    plt.xlabel('Muestras (#)')
   
    axes_hdl = plt.gca()
    axes_hdl.legend()
    axes_hdl.set_yticks(())
           
    plt.show()
 
###################################
# Regiones de interés sin ruido #
###################################
 
regs_interes = (
        np.array([5, 5.2]) *60*fs, # minutos a muestras
        np.array([12, 12.4]) *60*fs, # minutos a muestras
        np.array([15, 15.2]) *60*fs, # minutos a muestras
        )
 
for ii in regs_interes:
   
    # intervalo limitado de 0 a cant_muestras
    zoom_region = np.arange(np.max([0, ii[0]]), np.min([cant_muestras, ii[1]]), dtype='uint')
   
    plt.figure()
    plt.plot(zoom_region, ecg_one_lead[zoom_region], label='ECG', linewidth=2)
    #plt.plot(zoom_region, ECG_f_butt[zoom_region], label='Butterworth')
    plt.plot(zoom_region, ECG_f_win[zoom_region + demora], label='FIR Window')
   
    plt.title('filtro fir ventana cuadrada con ecg de ' + str(ii[0]) + ' a ' + str(ii[1]) )
    plt.ylabel('Adimensional')
    plt.xlabel('Muestras (#)')
   
    axes_hdl = plt.gca()
    axes_hdl.legend()
    axes_hdl.set_yticks(())
           
    plt.show()