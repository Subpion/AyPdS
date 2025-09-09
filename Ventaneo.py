


# -*- coding: utf-8 -*-
"""
Visualización de Ventanas en Dominio de Tiempo y Frecuencia
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

# Configuración de estilo para gráficos
plt.rcParams['figure.figsize'] = [10, 8]
plt.rcParams['font.size'] = 12

# Parámetros
N = 1000  # Longitud de la ventana
Fs = 1000 # Frecuencia de muestreo (Hz)
df = Fs / N  # Resolución en frecuencia (Δf = 1 Hz)

# Crear ventanas
hamming = sig.windows.hamming(N)
blackmanharris = sig.windows.blackmanharris(N)
flattop = sig.windows.flattop(N)

# Calcular respuestas en frecuencia
def calcular_respuesta_frecuencia(ventana, n_fft=None):
    if n_fft is None:
        n_fft = len(ventana)
    fft_result = np.fft.fft(ventana, n_fft)
    fft_result = np.fft.fftshift(fft_result)
    fft_magnitude = np.abs(fft_result) / np.max(np.abs(fft_result))
    return 20 * np.log10(fft_magnitude + 1e-10)  # dB

# Calcular respuestas
n_fft = 8192  # Mayor resolución para la respuesta en frecuencia
resp_hamming = calcular_respuesta_frecuencia(hamming, n_fft)
resp_blackmanharris = calcular_respuesta_frecuencia(blackmanharris, n_fft)
resp_flattop = calcular_respuesta_frecuencia(flattop, n_fft)

# Crear vector de frecuencia en Δf
frecs = np.linspace(-Fs/2, Fs/2, n_fft, endpoint=False)

# Crear figura con dos subplots
fig, axs = plt.subplots(2, 1)

# =============================================
# PRIMER SUBPLOT: Ventanas en el dominio del tiempo
# =============================================
n = np.arange(N)
axs[0].plot(n, hamming, label='Hamming', linewidth=1.5)
axs[0].plot(n, blackmanharris, label='Blackman-Harris', linewidth=1.5)
axs[0].plot(n, flattop, label='Flat-top', linewidth=1.5)
axs[0].set_title('Ventanas en el Dominio del Tiempo')
axs[0].set_xlabel('Muestras [n]')
axs[0].set_ylabel('Amplitud')
axs[0].grid(True)
axs[0].legend()

# =============================================
# SEGUNDO SUBPLOT: Respuestas en frecuencia (en Δf)
# =============================================
axs[1].plot(frecs, resp_hamming, label='Hamming', linewidth=1.5)
axs[1].plot(frecs, resp_blackmanharris, label='Blackman-Harris', linewidth=1.5)
axs[1].plot(frecs, resp_flattop, label='Flat-top', linewidth=1.5)

axs[1].set_title('Respuesta en Frecuencia (Eje en Δf)')
axs[1].set_xlabel('Frecuencia [Hz] (Δf = {:.2f} Hz)'.format(df))
axs[1].set_ylabel('Magnitud [dB]')
axs[1].set_xlim(-50, 50)  # Zoom alrededor de frecuencia cero
axs[1].set_ylim(-120, 5)
axs[1].grid(True)
axs[1].legend()

plt.tight_layout()
plt.show()

# # =============================================
# # ANÁLISIS DE PARÁMETROS DE LAS VENTANAS
# # =============================================
# print("=" * 60)
# print("COMPARACIÓN DE PARÁMETROS DE VENTANAS")
# print("=" * 60)
# print(f"Resolución en frecuencia (Δf): {df:.2f} Hz")
# print()

# # Calcular ancho de lóbulo principal
# def calcular_ancho_lobulo_principal(respuesta, frecuencias, nivel_db=-3):
#     # Encontrar el pico central
#     idx_centro = len(respuesta) // 2
#     magnitud_central = respuesta[idx_centro]
#     nivel_absoluto = magnitud_central + nivel_db
    
#     # Buscar cruces por derecha
#     idx_derecha = idx_centro
#     while idx_derecha < len(respuesta)-1 and respuesta[idx_derecha] > nivel_absoluto:
#         idx_derecha += 1
    
#     # Buscar cruces por izquierda
#     idx_izquierda = idx_centro
#     while idx_izquierda > 0 and respuesta[idx_izquierda] > nivel_absoluto:
#         idx_izquierda -= 1
    
#     ancho_hz = frecuencias[idx_derecha] - frecuencias[idx_izquierda]
#     ancho_df = ancho_hz / df  # Convertir a múltiplos de Δf
    
#     return ancho_hz, ancho_df

# # Calcular para cada ventana
# ancho_hz_h, ancho_df_h = calcular_ancho_lobulo_principal(resp_hamming, frecs)
# ancho_hz_bh, ancho_df_bh = calcular_ancho_lobulo_principal(resp_blackmanharris, frecs)
# ancho_hz_ft, ancho_df_ft = calcular_ancho_lobulo_principal(resp_flattop, frecs)

# print("Ancho de lóbulo principal (-3 dB):")
# print(f"  Hamming:          {ancho_hz_h:.2f} Hz ({ancho_df_h:.2f} Δf)")
# print(f"  Blackman-Harris:  {ancho_hz_bh:.2f} Hz ({ancho_df_bh:.2f} Δf)")
# print(f"  Flat-top:         {ancho_hz_ft:.2f} Hz ({ancho_df_ft:.2f} Δf)")
# print()

# # Calcular atenuación del lóbulo lateral más alto
# def calcular_atenuacion_lobulos(respuesta, frecuencias, margen_hz=20):
#     idx_centro = len(respuesta) // 2
    
#     # Buscar máximo lóbulo lateral (excluyendo lóbulo principal)
#     # Lado derecho
#     inicio_derecha = idx_centro + int(margen_hz / df)  # Excluir lóbulo principal
#     max_derecha = np.max(respuesta[inicio_derecha:])
    
#     # Lado izquierdo
#     fin_izquierda = idx_centro - int(margen_hz / df)  # Excluir lóbulo principal
#     max_izquierda = np.max(respuesta[:fin_izquierda])
    
#     return max(max_izquierda, max_derecha)

# atenuacion_h = calcular_atenuacion_lobulos(resp_hamming, frecs)
# atenuacion_bh = calcular_atenuacion_lobulos(resp_blackmanharris, frecs)
# atenuacion_ft = calcular_atenuacion_lobulos(resp_flattop, frecs)

# print("Atenuación del lóbulo lateral más alto:")
# print(f"  Hamming:          {atenuacion_h:.2f} dB")
# print(f"  Blackman-Harris:  {atenuacion_bh:.2f} dB")
# print(f"  Flat-top:         {atenuacion_ft:.2f} dB")
# print()

# # Mostrar resumen comparativo
# print("RESUMEN COMPARATIVO:")
# print("  - Hamming: Lóbulo principal más estrecho pero menor atenuación de lóbulos laterales")
# print("  - Blackman-Harris: Buen equilibrio entre ancho de lóbulo y atenuación")
# print("  - Flat-top: Mayor atenuación de lóbulos laterales pero lóbulo principal más ancho")