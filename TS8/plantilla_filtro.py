import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

#--------plantilla de diseno-----------

wp= [1, 35]#frecuancia de corte/paso hz
ws= [0.1 , 40]  #frecuencia de stop/detenida hz

alpha_p= 1 #atenuacion a la wp de corte alfa max 
alpha_s= 40 #atenuacion a la ws de corte alfa min 
fs= 1000
# aprox a modulo

f_aprox = "butter"
#f_aprox = "cheby1"
# f_aprox = "cheby2"
#f_aprox = "cauer"

#aprox a fase 
#f_aprox = "bessel"

#------diseno de filtro analogico------
mi_sos=signal.iirdesign(wp=wp,ws=ws,gpass=alpha_p,
                     gstop=alpha_s,
                     analog=False,
                     ftype = f_aprox,
                     output= "sos",fs=fs)
#por defecto la frecuencia de muestreo es 2 por lo que no tomaria la wp y ws 

w, h=signal.freqz_sos(mi_sos,fs=fs,worN=np.logspace(-2,2,1000)) #de 10^-2 a 10^2        
#w, h=signal.freqs(b,a)
# --- Cálculo de fase y retardo de grupo ---
phase = np.unwrap(np.angle(h))
# Retardo de grupo = -dφ/dω
w_rad=w/(fs/2) *np.pi
gd = -np.diff(phase) / np.diff(w_rad)

# --- Polos y ceros ---
z, p, k = signal.sos2zpk(mi_sos)

# --- Gráficas ---
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
plt.subplot(2,2,4)
plt.plot(np.real(p), np.imag(p), 'x', markersize=10, label='Polos')
if len(z) > 0:
                   plt.plot(np.real(z), np.imag(z), 'o', markersize=10, fillstyle='none', label='Ceros')
plt.axhline(0, color='k', lw=0.5)
plt.axvline(0, color='k', lw=0.5)
plt.title('Diagrama de Polos y Ceros (plano s)')
plt.xlabel('σ [rad/s]')
plt.ylabel('jω [rad/s]')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
