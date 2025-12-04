import matplotlib.pyplot as plt
import numpy as np
import scipy.fft as fft
import scipy.signal as signal

# CONCEPTION DU FILTRE

N = 110  # Ordre de 310 -> N+1 coefficients
alpha = N // 2  # 55
wc = 0.25 * np.pi

# Réponse impulsionnelle du filtre idéal
hd = np.zeros(N + 1)
for i in range(N + 1):
    if i == alpha:
        hd[i] = wc / np.pi
    else:
        hd[i] = np.sin((i-alpha) * wc)/(np.pi*(i-alpha))

# Fenêtre de Hanning
n = np.arange(N + 1)
w = 0.54 - 0.46 * np.cos(2 * np.pi * n / N)

# Réponse impulsionnelle du filtre
h = hd * w

# Réponse en fréquences du filtre
omega, H = signal.freqz(h)
freq = omega / np.pi

plt.figure(figsize=(10, 4))
plt.plot(freq, np.abs(H))
plt.axvline(0.22, color="r", ls="--")
plt.axvline(0.28, color="r", ls="--")
plt.title("Réponse en fréquences")
plt.xlabel("Fréquences (ω/π)")
plt.ylabel("Amplitude")
# plt.show()

# TEST DU FILTRE (domaine temporel)

N = 2000
n = np.arange(N)

x = np.sin(0.1 * np.pi * n) + 0.5 * np.sin(0.6 * np.pi * n)
y = np.convolve(x, h, mode="same")

plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(n[1000:1500], x[1000:1500])
plt.title("Signal original (extrait)")
plt.ylabel("x[n]")

plt.subplot(2, 1, 2)
plt.plot(n[1000:1500], y[1000:1500])
plt.title("Signal filtré (extrait)")
plt.xlabel("n")
plt.ylabel("y[n]")

plt.tight_layout()
plt.show()

mean = 0
scale = 1
noise = np.random.normal(mean, scale, size=N)

noise_filtre = np.convolve(noise, h, mode="same")
x = fft.rfftfreq(N) * 2
noise_filtre_fft = fft.rfft(noise_filtre)
noise_fft = fft.rfft(noise)

plt.plot(x, np.abs(noise_fft),color='orange')
plt.plot(x,  np.abs(noise_filtre_fft),color='royalblue')
plt.title("Bruit Blanc + Filtre")
plt.show()