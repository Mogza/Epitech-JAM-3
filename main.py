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
status = ""

def afficher_texte_centre(texte, color, x, y):
    texte_surface = police.render(texte, True, color)
    texte_rect = texte_surface.get_rect()
    texte_rect.centerx = largeur * (x / 100)
    texte_rect.centery = hauteur * (y / 100)
    fenetre.blit(texte_surface, texte_rect)

def demarrer_jeu():
    global score, streak, mstreak, status
    mot_actuel = random.choice(mots)
    saisie_utilisateur = ""
    temps_debut = time.time()

    while True:
        fenetre.fill((25, 25, 25))
        afficher_texte_centre(mot_actuel, (255, 255, 255), 50, 40)
        afficher_texte_centre(saisie_utilisateur, (0, 225, 0), 50, 50)
        afficher_texte_centre(status, (0, 0, 255), 50, 60)
        afficher_texte_centre(str(score), (0, 225, 0), 6, 5)
        afficher_texte_centre(str(streak), (255, 0, 0), 6, 10)

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
                    status = "+" + str(streak * len(mot_actuel))
                    print(time.time() - temps_debut)
                    return demarrer_jeu()
                elif event.key == pygame.K_RETURN and saisie_utilisateur != mot_actuel:
                    pygame.display.update()
                    if streak > mstreak:
                        mstreak = streak
                    streak = 0
                    status = "-"
                    print(time.time() - temps_debut)
                    return demarrer_jeu()

        pygame.display.update()

def menu_principal():
    while True:
        fenetre.fill((255, 255, 255))
        afficher_texte_centre("MENU", (0, 0, 0), 50, 30)
        
        bouton_demarrer = pygame.Rect(largeur / 2 - 100, hauteur / 2 - 50, 200, 50)
        bouton_quitter = pygame.Rect(largeur / 2 - 100, hauteur / 2 + 20, 200, 50)

        pygame.draw.rect(fenetre, (0, 255, 0), bouton_demarrer)
        pygame.draw.rect(fenetre, (255, 0, 0), bouton_quitter)

        afficher_texte_centre("START", (255, 255, 255), 50, 48)
        afficher_texte_centre("EXIT", (255, 255, 255), 50, 54)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_demarrer.collidepoint(event.pos):
                    demarrer_jeu()
                if bouton_quitter.collidepoint(event.pos):
                    pygame.quit()
                    return

        pygame.display.update()

menu_principal()