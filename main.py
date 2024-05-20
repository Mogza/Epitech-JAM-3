from time import time

import pygame
import sys
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
hp = 3


def afficher_texte_centre(texte, color, x, y):
    texte_surface = police.render(texte, True, color)
    texte_rect = texte_surface.get_rect()
    texte_rect.centerx = largeur * (x / 100)
    texte_rect.centery = hauteur * (y / 100)
    fenetre.blit(texte_surface, texte_rect)


def afficher_page_defaite():
    bouton_menu = pygame.Rect(largeur // 2 - LARGEUR_BOUTON // 2, hauteur // 2 - HAUTEUR_BOUTON // 2, LARGEUR_BOUTON, HAUTEUR_BOUTON)
    bouton_rejouer = pygame.Rect(largeur // 2 - LARGEUR_BOUTON // 2, hauteur // 2 + 80, LARGEUR_BOUTON, HAUTEUR_BOUTON)

    while True:
        for y in range(hauteur):
            couleur = (
                0 + (105 - 0) * y / hauteur,
                105 + (105 - 105) * y / hauteur,
                105 + (105 - 105) * y / hauteur
            )
            pygame.draw.line(fenetre, couleur, (0, y), (largeur, y))

        afficher_texte_centre_menu("Défaite!", (255, 0, 0), largeur // 2, hauteur // 4, TAILLE_POLICE_MENU)

        if bouton_menu.collidepoint(pygame.mouse.get_pos()):
            afficher_bouton("Retour au menu", (0, 105, 105), bouton_menu, 10)
        else:
            afficher_bouton("Retour au menu", (0, 225, 225), bouton_menu, 10)

        if bouton_rejouer.collidepoint(pygame.mouse.get_pos()):
            afficher_bouton("Rejouer", (0, 105, 105), bouton_rejouer, 10)
        else:
            afficher_bouton("Rejouer", (0, 225, 225), bouton_rejouer, 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_menu.collidepoint(event.pos):
                    return menu_principal()
                elif bouton_rejouer.collidepoint(event.pos):
                    return demarrer_jeu()

        pygame.display.flip()


def demarrer_jeu():
    global score, streak, mstreak, status, hp
    mot_actuel = random.choice(mots)
    saisie_utilisateur = ""
    temps_debut = time.time()

    while True:
        fenetre.fill((0, 105, 105))
        afficher_texte_centre(mot_actuel, (255, 255, 255), 50, 40)
        afficher_texte_centre(saisie_utilisateur, (0, 225, 0), 50, 50)
        afficher_texte_centre(status, (255, 0, 0), 50, 60)
        afficher_texte_centre("Score : " + str(score), (0, 225, 0), 10, 5)
        afficher_texte_centre("Vies : ", (0, 0, 255), 10, 15)
        draw_life_points(hp)
        if status != "":
            draw_streak_screen()
            draw_streak_flamme()
        if hp == 0:
            score = 0
            streak = 0
            status = ""
            hp = 3
            afficher_page_defaite()
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
                    status = str(streak)
                    return demarrer_jeu()
                elif event.key == pygame.K_RETURN and saisie_utilisateur != mot_actuel:
                    pygame.display.update()
                    if streak > mstreak:
                        mstreak = streak
                    streak = 0
                    status = ""
                    hp -= 1
                    return demarrer_jeu()

        pygame.display.update()


COULEUR_BLEU = (51, 51, 255)
COULEUR_VIOLET = (153, 51, 255) 


def draw_life_points(life_points):
    image = pygame.image.load("assets/Flamme.png").convert_alpha()
    image = pygame.transform.scale(image, (62, 144))
    y = 275
    i = 0
    while i < life_points :
        fenetre.blit(image, (y, 75))
        i = i + 1
        y = y + 72


def draw_streak_screen():
    image = pygame.image.load("assets/Fire.png").convert_alpha()
    image = pygame.transform.scale(image, (1000, 438))
    fenetre.blit(image, (405, 642))


def draw_streak_flamme():
    image = pygame.image.load("assets/Streak_flamme.png").convert_alpha()
    image = pygame.transform.scale(image, (75, 75))
    fenetre.blit(image, (990, 605))


def afficher_bouton(texte, couleur, rect, radius):
    pygame.draw.rect(fenetre, couleur, rect, border_radius=radius)
    afficher_texte_centre_menu(texte, (255, 255, 255), rect.centerx, rect.centery, 30)


LARGEUR_BOUTON = 250
HAUTEUR_BOUTON = 80


def afficher_texte_centre_menu(texte, color, x, y, taille_police):
    font = pygame.font.Font(None, taille_police)
    text = font.render(texte, True, color)
    text_rect = text.get_rect(center=(x, y))
    fenetre.blit(text, text_rect)


TAILLE_POLICE_MENU = 60


def menu_principal():
    while True:
        for y in range(hauteur):
            couleur = (
                0 + (105 - 0) * y / hauteur,
                105 + (105 - 105) * y / hauteur,
                105 + (105 - 105) * y / hauteur
            )
            pygame.draw.line(fenetre, couleur, (0, y), (largeur, y))

        afficher_texte_centre_menu("MENU", (255, 255, 255), largeur // 2, hauteur // 4, TAILLE_POLICE_MENU)
        
        bouton_demarrer = pygame.Rect(largeur // 2 - LARGEUR_BOUTON // 2, hauteur // 2 - HAUTEUR_BOUTON // 2, LARGEUR_BOUTON, HAUTEUR_BOUTON)
        bouton_quitter = pygame.Rect(largeur // 2 - LARGEUR_BOUTON // 2, hauteur // 2 + 80, LARGEUR_BOUTON, HAUTEUR_BOUTON)

        if bouton_demarrer.collidepoint(pygame.mouse.get_pos()):
            afficher_bouton("START", (0, 105, 105), bouton_demarrer, 10)
        else:
            afficher_bouton("START", (0, 225, 225), bouton_demarrer, 10)
        
        if bouton_quitter.collidepoint(pygame.mouse.get_pos()):
            afficher_bouton("EXIT", (0, 105, 105), bouton_quitter, 10)
        else:
            afficher_bouton("EXIT", (0, 225, 225), bouton_quitter, 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_demarrer.collidepoint(event.pos):
                    demarrer_jeu()
                if bouton_quitter.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


menu_principal()


pygame.quit()
