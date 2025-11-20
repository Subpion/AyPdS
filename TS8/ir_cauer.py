
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

wp= [0.8, 35]#frecuancia de corte/paso hz
ws= [0.1 , 40]  #frecuencia de stop/detenida hz

alpha_p= 1/2 #atenuacion a la wp de corte alfa max /divido por dos por el filt filt
alpha_s= 40/2 #atenuacion a la ws de corte alfa min 
fs= 1000
# aprox a modulo



#aprox a fase 
#f_aprox = "bessel"

#------diseno de filtro analogico------

f_aprox = "cauer"
mi_sos_cauer=signal.iirdesign(wp=wp,ws=ws,gpass=alpha_p,
                     gstop=alpha_s,
                     analog=False,
                     ftype = f_aprox,
                     output= "sos",fs=fs)


#por defecto la frecuencia de muestreo es 2 por lo que no tomaria la wp y ws 



ecg_filtrado_cauer=signal.sosfilt(mi_sos_cauer , ecg_one_lead)




# ---------------------------------------------------
# 2. RESPUESTA EN FRECUENCIA: Módulo y Fase
# ---------------------------------------------------

w, h = signal.sosfreqz(mi_sos_cauer , worN=2048, fs=fs)

# Módulo en dB
modulo = 20 * np.log10(np.abs(h))

# Fase en radianes
fase = np.unwrap(np.angle(h))


# ---------------------------------------------------
# 3. RETARDO DE GRUPO
# ---------------------------------------------------

w_gd, gd = signal.group_delay((signal.sos2tf(mi_sos_cauer )), fs=fs)


# ---------------------------------------------------
# 4. DIAGRAMA DE POLOS Y CEROS
# ---------------------------------------------------

z, p, k = signal.sos2zpk(mi_sos_cauer )


# ---------------------------------------------------
# 5. GRÁFICAS
# ---------------------------------------------------

plt.figure(1,figsize=(12,10))

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

ecg_filtrado_cauer=signal.sosfiltfilt(mi_sos_cauer
                                   , ecg_one_lead)

plt.figure(2)


plt.plot(ecg_filtrado_cauer,label = "cauer")

plt.plot(ecg_one_lead,label="original")

plt.legend()
