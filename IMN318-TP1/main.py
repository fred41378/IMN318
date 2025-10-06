import numpy as np
from numpy.linalg import norm
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq
import pygame
import sys

fichier_a_lire = "./fichiers_sonores/toxic.wav"

# Ouverture du fichier musical pour l'analyse
fs, data = wavfile.read(fichier_a_lire)

# Séparation des canaux gauche-droite
#TODO AJOUTER DU CODE ICI
data_left = data[:,0]
data_right = data[:,1]


# Pour des fins de manipulation, ramener les valeurs des cannaux gauche-droite entre -1 et 1
#TODO AJOUTER DU CODE ICI
data_left = data_left/np.max(data_left)
data_right = data_right/np.max(data_right)

# Initialisation de la fenêtre graphique
pygame.init()
display = (800, 600)
surface = pygame.display.set_mode(display)

# Ouverture du fichier musical pour la lecture
pygame.mixer.music.load(fichier_a_lire)
pygame.mixer.music.play(0)
play_time = pygame.time.get_ticks()

color = (255, 255, 255)  # affichage en blanc

t = pygame.time.get_ticks()
getTicksLastFrame = t

# Paramètres pour la visualisation temporelle
current_height_left = 0
current_height_right = 0

# Paramètres pour la visualisation fréquentielle
nb_columns = 30
deltaFreq = int(6000 / nb_columns)
bars_top = np.zeros((nb_columns, 1))
bars_top_old = bars_top

# Dernière touche appuyée sur le calvier (t = analyse temporelle, f = analyse fréquentielle, q = quitter)
last_key = pygame.K_t

# Boucle principale
while True:
    # Interaction avec le clavier
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_t:
                print("Analyse temporelle")
                last_key = pygame.K_t
            elif event.key == pygame.K_f:
                print("Analyse fréquentielle")
                last_key = pygame.K_f

    # Fond noir
    surface.fill((0, 0, 0))

    # Dernière touche = t -> Analyse temporelle
    if last_key == pygame.K_t:
        # Gestion du temps pour garder l'affichage synchronisé avec la musique
        # "t" est le temps actuel
        t = pygame.time.get_ticks() - play_time
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        #TODO AJOUTER DU CODE ICI
        # chunk_left et chunk_right sont des tableaux contenant les données temporelles à analyser
        # l'intervalle d'analyse contient les valeurs entre t - 0,01s et t + 0,01s
        chunk_left = np.arange(t-0.1, t+0.1)
        chunk_right = np.arange(t-0.1, t+0.1)

        #TODO AJOUTER DU CODE ICI
        # norm_left et norm_right correspondent à la racine carrée de la somme des carrés des éléments
        # de chunk_left et chunk_right, respectivement
        norm_left = np.sqrt(sum(chunk_left**2))
        norm_right = 3

        # Gauche
        desired_height_left = 30 * norm_left
        speed = (desired_height_left - current_height_left) / 0.1
        new_height_left = current_height_left + speed * deltaTime
        current_height_left = new_height_left

        # Droit
        desired_height_right = 30 * norm_right
        speed = (desired_height_right - current_height_right) / 0.1
        new_height_right = current_height_right + speed * deltaTime
        current_height_right = new_height_right

        # Construction des colonnes
        points = [(200, 500),
                  (200, 500-new_height_left),
                  (300, 500-new_height_left),
                  (300, 500),
                  (500, 500),
                  (500, 500-new_height_right),
                  (600, 500-new_height_right),
                  (600, 500)]

        # Affichage
        pygame.draw.polygon(surface, color, points)

    elif last_key == pygame.K_f:
        # Gestion du temps pour garder l'affichage synchronisé avec la musique
        # "t" est le temps actuel
        t = pygame.time.get_ticks() - play_time
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        #TODO AJOUTER DU CODE ICI
        # chunk_left et chunk_right sont des tableaux contenant les données temporelles à analyser
        # l'intervalle d'analyse contient les valeurs entre t - 0,25s et t + 0,25s
        chunk_left = 0
        chunk_right = 0

        #TODO AJOUTER DU CODE ICI
        # chunk_left_hat et chunk_right_hat sont les transformées de Fourier de chunk_left et chunk_right, resp.
        chunk_left_hat = 0
        chunk_right_hat = 0

        #TODO AJOUTER DU CODE ICI
        # chunk_amp est la moyenne des spectres amplitudes de chunk_left_hat et chunk_right_hat
        chunk_amp = 0

        #TODO AJOUTER DU CODE ICI
        # deltaPosition représente l'écart "en position" entre le début et la fin des fréquences
        # associées à une colonne en fonction de l'écart "en fréquence" deltaFreq
        deltaPosition = 0

        # Construction des colonnes
        points = [(25, 500)]
        for i in range(nb_columns):
            #TODO AJOUTER DU CODE ICI
            # amp représente la moyenne des amplitudes des fréquences associées à la i-ième colonne
            amp = 0

            # Conversion des amplitudes en décibels
            amp_db = np.clip(20 * np.log10(amp / 32768), -80, 0) + 80
            current_height = bars_top_old[i]
            desired_height = 5 * amp_db
            speed = (desired_height - current_height) / 0.04
            bars_top[i] = current_height + speed * deltaTime
            points.append((25 + i * 25, 500 - bars_top[i, 0]))
            points.append((25 + (i + 1) * 25, 500 - bars_top[i, 0]))
        points.append((775, 500))

        # Affichage
        pygame.draw.polygon(surface, color, points)

    # Rafraichissement
    pygame.display.flip()
