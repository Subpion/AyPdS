# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 17:30:36 2025

@author: angel
"""

import numpy as np
import matplotlib.pyplot as plt

def mi_funcion_sen(vmax=1, dc=0, ff=1, ph=0, nn=1000, fs=1000):

    # Vector de tiempo
    tt = np.arange(0, nn) / fs
    velang=2 * np.pi * ff
    # Señal senoidal
    xx = dc + vmax * np.sin(velang * tt + ph)

    return tt, xx


# Ejemplo de uso:
if __name__ == "__main__":
    N = 1000     # cantidad de muestras
    fs = 1000   # frecuencia de muestreo en Hz
    ffs= 2
    vmaxs= 2
    dcs= 0
    fas=0
    # Llamar a la función
    tt, xx = mi_funcion_sen(vmax=vmaxs, dc=dcs, ff=ffs, ph=fas, nn=N, fs=fs)

    # Graficar
    plt.figure()
    plt.plot(tt, xx)
    plt.title("Señal Senoidal")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud [V]")
    plt.show()