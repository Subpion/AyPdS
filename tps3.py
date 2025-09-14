import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft

# %% Función senoidal
def sen(ff, nn, vmax=1, dc=0, ph=0, fs=2):
    n = np.arange(0, nn)
    tt = n/fs
    w0 = 2 * np.pi * ff
    xx = dc + vmax * np.sin(w0 * tt + ph)
    return tt, xx

# %% Parámetros
N = 1000
Fs = N
df = Fs/N

# Definimos las tres frecuencias pedidas
f1 = (N/4) * df
f2 = (N/4 + 0.25) * df
f3 = (N/4 + 0.5) * df

# %% Señales
_, x1 = sen(ff=f1, nn=N, fs=Fs)
_, x2 = sen(ff=f2, nn=N, fs=Fs)
_, x3 = sen(ff=f3, nn=N, fs=Fs)

# Normalización a potencia unitaria (varianza = 1)
x1 = x1 / np.sqrt(np.var(x1))
x2 = x2 / np.sqrt(np.var(x2))
x3 = x3 / np.sqrt(np.var(x3))

# %% FFT y PSD
X1 = fft(x1)
X2 = fft(x2)
X3 = fft(x3)

PSD1 = (1/N) * np.abs(X1)**2
PSD2 = (1/N) * np.abs(X2)**2
PSD3 = (1/N) * np.abs(X3)**2

frec = np.arange(N) * df

# %% a) Graficar las PSD
plt.figure(figsize=(10,5))
plt.plot(frec, PSD1, label="k0 = N/4")
plt.plot(frec, PSD2, label="k0 = N/4 + 0.25")
plt.plot(frec, PSD3, label="k0 = N/4 + 0.5")
plt.xlim(0, Fs/2)
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Densidad Espectral de Potencia")
plt.title("PSD de senoidales con ligera desintonía")
plt.legend()
plt.grid(True)
plt.show()

# %% b) Verificación de Parseval
Et1 = np.sum(np.abs(x1)**2)
Ef1 = (1/N)*np.sum(np.abs(X1)**2)

Et2 = np.sum(np.abs(x2)**2)
Ef2 = (1/N)*np.sum(np.abs(X2)**2)

Et3 = np.sum(np.abs(x3)**2)
Ef3 = (1/N)*np.sum(np.abs(X3)**2)

print("Verificación de Parseval:")
print(f" Señal k0=N/4      -> diferencia = {Et1 - Ef1:.5e}")
print(f" Señal k0=N/4+0.25 -> diferencia = {Et2 - Ef2:.5e}")
print(f" Señal k0=N/4+0.5  -> diferencia = {Et3 - Ef3:.5e}")

# %% c) Zero padding
Npad = 9 * N
frec_pad = np.arange(Npad) * Fs / Npad

X3z = fft(np.pad(x3, (0, Npad-N)))
PSD3z = (1/Npad) * np.abs(X3z)**2

plt.figure(figsize=(10,5))
plt.plot(frec, PSD3, ':x', label="Sin zero-padding")
plt.plot(frec_pad, PSD3z, label="Con zero-padding (9N)")
plt.xlim(f3-10, f3+10)  # zoom alrededor de la frecuencia
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Densidad Espectral de Potencia")
plt.title("Efecto del Zero-padding en la PSD")
plt.legend()
plt.grid(True)
plt.show()



