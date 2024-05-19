import pygame
import random
import time
import json
import re

pygame.init()

def extraire_noms_filtres(fichier_json):
    with open(fichier_json, "r") as f:
        data = json.load(f)
    pattern = re.compile(r'^[a-z]+$')
    noms_filtres = [nom for element in data if "name" in element.keys() for nom in [element["name"]] if pattern.match(nom.lower())]
    return noms_filtres


info_objet = pygame.display.Info()
largeur, hauteur = info_objet.current_w, info_objet.current_h
fenetre = pygame.display.set_mode((largeur, hauteur), pygame.FULLSCREEN)
mots = extraire_noms_filtres("assets/words.json")
pygame.display.set_caption("JAM 3")
police = pygame.font.Font("assets/ARCADE_R.TTF", 35)
score = 0
streak = 0
mstreak = 0

def afficher_texte_centre(texte, x, y):
    texte_surface = police.render(texte, True, (0, 0, 0))
    texte_rect = texte_surface.get_rect()
    texte_rect.centerx = largeur * (x / 100)
    texte_rect.centery = hauteur * (y / 100)
    fenetre.blit(texte_surface, texte_rect)

def demarrer_jeu():
    global score, streak, mstreak
    mot_actuel = random.choice(mots)
    saisie_utilisateur = ""
    temps_debut = time.time()

    while True:
        fenetre.fill((255, 255, 255))
        afficher_texte_centre(mot_actuel, 50, 45)
        afficher_texte_centre(saisie_utilisateur, 50, 55)
        afficher_texte_centre(str(score), 6, 5)
        afficher_texte_centre(str(streak), 6, 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    saisie_utilisateur = saisie_utilisateur[:-1]
                elif 'a' <= event.unicode <= 'z':
                    saisie_utilisateur += event.unicode
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key == pygame.K_RETURN and saisie_utilisateur == mot_actuel:
                    pygame.display.update()
                    streak += 1
                    score += streak * len(mot_actuel)
                    return demarrer_jeu()
                elif event.key == pygame.K_RETURN and saisie_utilisateur != mot_actuel:
                    pygame.display.update()
                    if streak > mstreak:
                        mstreak = streak
                    streak = 0
                    return demarrer_jeu()

        pygame.display.update()

demarrer_jeu()
