

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
ripple = 1 /2# dB
atenuacion = 40 /2# dB
 
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


f_aprox = "butter"
mi_sos_butt=signal.iirdesign(wp=[wp1,wp2],
                              ws=[ws1,ws2],
                              gpass=ripple,
                              gstop=atenuacion,
                              analog=False,
                              ftype = f_aprox,
                              output= "sos",fs=fs)

ECG_f_win=signal.sosfiltfilt(mi_sos_butt , ecg_one_lead)


##########################
# respuesta en frecuencia#
##########################

w, h = signal.sosfreqz(mi_sos_butt , worN=2048, fs=fs)

# Módulo en dB
modulo = 20 * np.log10(np.abs(h))

# Fase en radianes
fase = np.unwrap(np.angle(h))


# ---------------------------------------------------
# 3. RETARDO DE GRUPO
# ---------------------------------------------------

w_gd, gd = signal.group_delay((signal.sos2tf(mi_sos_butt )), fs=fs)


# ---------------------------------------------------
# 4. DIAGRAMA DE POLOS Y CEROS
# ---------------------------------------------------

z, p, k = signal.sos2zpk(mi_sos_butt)

plt.figure(figsize=(12,10))

# --- Magnitud ---
plt.subplot(2,2,1)
plt.plot(w, modulo)
plt.title("Módulo (dB)")
plt.ylabel("Amplitud (dB)")
plt.xlabel("Frecuencia [Hz]")
plt.grid()

# --- Fase ---
plt.subplot(2,2,2)
plt.plot(w, fase)
plt.title("Fase (rad)")
plt.ylabel("Fase (rad)")
plt.xlabel("Frecuencia [Hz]")
plt.grid()

# --- Retardo de grupo ---
plt.subplot(2,2,3)
plt.plot(w_gd, gd)
plt.title("Retardo de Grupo")
plt.ylabel("Tiempo [samples]")
plt.xlabel("Frecuencia [Hz]")
plt.grid()

# --- Polos y ceros ---
plt.subplot(2,2,4)
plt.scatter(np.real(z), np.imag(z), marker='o', label="Ceros")
plt.scatter(np.real(p), np.imag(p), marker='x', label="Polos")
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.title("Diagrama de Polos y Ceros")
plt.xlabel("Parte Real")
plt.ylabel("Parte Imaginaria")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()

###################################
# Regiones de interés sin ruido #
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
    plt.plot(zoom_region, ECG_f_win[zoom_region ], label='FIR Window')
   
    plt.title('filtro ir aproximacion butterworth con ecg de' + str(ii[0]) + ' a ' + str(ii[1]) )
    plt.ylabel('Adimensional')
    plt.xlabel('Muestras (#)')
   
    axes_hdl = plt.gca()
    axes_hdl.legend()
    axes_hdl.set_yticks(())
           
    plt.show()
 
###################################
# Regiones de interés con ruido #
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
    plt.plot(zoom_region, ECG_f_win[zoom_region ], label='FIR Window')
   
    plt.title('filtro ir aproximacion butterworth con ecg de' + str(ii[0]) + ' a ' + str(ii[1]) )
    plt.ylabel('Adimensional')
    plt.xlabel('Muestras (#)')
   
    axes_hdl = plt.gca()
    axes_hdl.legend()
    axes_hdl.set_yticks(())
           
    plt.show()