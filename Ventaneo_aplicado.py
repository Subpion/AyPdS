import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft
import scipy.signal.windows as win

# ------------------------------
# Definir señal base
# ------------------------------
def sen(ff, nn, vmax=1, dc=0, ph=0, fs=2):
    n = np.arange(0, nn)
    tt = n / fs
    w0 = 2 * np.pi * ff
    xx = dc + vmax * np.sin(w0 * tt + ph)
    return tt, xx

N = 1000
Fs = N
df = Fs / N

# Senoide en frecuencia no entera -> genera leakage
t3, x3 = sen(ff=((N/4) + 0.5) * df, nn=N, fs=Fs)

# ------------------------------
# Definir ventanas
# ------------------------------
hamming = win.hamming(N)
blackmanharris = win.blackmanharris(N)
flattop = win.flattop(N)

# Aplicar ventanas
x_hamming = x3 * hamming
x_blackmanharris = x3 * blackmanharris
x_flattop = x3 * flattop

# ------------------------------
# Calcular FFTs
# ------------------------------
X_hamming = np.abs(fft(x_hamming)) / N
X_blackmanharris = np.abs(fft(x_blackmanharris)) / N
X_flattop = np.abs(fft(x_flattop)) / N

frec = np.arange(N) * df

# ------------------------------
# Graficar espectros
# ------------------------------
plt.figure(figsize=(10,6))
plt.plot(frec, 20*np.log10(X_hamming), label="Hamming")
plt.plot(frec, 20*np.log10(X_blackmanharris), label="Blackman-Harris")
plt.plot(frec, 20*np.log10(X_flattop), label="Flat-top")

plt.xlim(200, 300)  # acercamos la zona de interés
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Magnitud [dB]")
plt.title("Efecto del Ventaneo en la FFT (N=1000, fs=N)")
plt.legend()
plt.grid(True)
plt.show()

# ------------------------------
# Graficar las ventanas en el tiempo
# ------------------------------
plt.figure(figsize=(10,5))
plt.plot(hamming, label="Hamming")
plt.plot(blackmanharris, label="Blackman-Harris")
plt.plot(flattop, label="Flat-top")
plt.title("Formas de las ventanas")
plt.xlabel("Muestras [n]")
plt.ylabel("Amplitud")
plt.legend()
plt.grid(True)
plt.show()




