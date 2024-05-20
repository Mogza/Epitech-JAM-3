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
largeur, hauteur = 1920, 1080
fenetre = pygame.display.set_mode((largeur, hauteur), pygame.FULLSCREEN)
mots = extraire_noms_filtres("assets/words.json")
pygame.display.set_caption("JAM 3")
police = pygame.font.Font("assets/ARCADE_R.TTF", 35)
score = 0
streak = 0
mstreak = 0
streak_detector = 0
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
        afficher_texte_centre_menu("Best Score : " + str(get_best_score()), (0, 225, 0), 1650, 50, TAILLE_POLICE_MENU)
        afficher_texte_centre_menu("Your Score : " + str(get_last_score()), (0, 225, 0), largeur // 2, (hauteur // 4) + 50, TAILLE_POLICE_MENU)

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
    global score, streak, mstreak, streak_detector, status, hp
    mot_actuel = random.choice(mots)
    saisie_utilisateur = ""
    start_ticks = pygame.time.get_ticks()
    background = pygame.image.load("assets/Background.jpg").convert_alpha()
    background = pygame.transform.scale(background, (1920, 1080))

    while True:
        fenetre.fill((0, 0, 0))
        fenetre.blit(background, (0, 0))
        seconds = (pygame.time.get_ticks()-start_ticks)/1000
        afficher_texte_centre(mot_actuel, (255, 255, 255), 50, 40)
        afficher_texte_centre(saisie_utilisateur, (0, 225, 0), 50, 50)
        afficher_texte_centre(status, (180, 6, 6), 50, 60)
        afficher_texte_centre("Score : " + str(score), (0, 225, 0), 12, 5)
        afficher_texte_centre("Vies : ", (255, 127, 0), 10, 15)
        afficher_texte_centre(str(int((5 - seconds) + 1)) + " secondes", (180, 6, 6), 50, 30)
        afficher_texte_centre("Best Score : " + str(get_best_score()), (0, 225, 0), 80, 5)
        draw_life_points(hp)

        if status != "":
            draw_streak_screen()
            draw_streak_flamme()
        if hp == 0:
            write_last_score(score)
            write_best_score(score)
            score = 0
            streak = 0
            status = ""
            hp = 3
            streak_detector = 0
            afficher_page_defaite()
        if seconds > 5:
            pygame.display.update()
            if streak > mstreak:
                mstreak = streak
            streak = 0
            status = ""
            hp -= 1
            return demarrer_jeu()
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
                    if streak_detector >= 3:
                        streak += 1
                        score += streak * len(mot_actuel)
                        status = str(streak)
                    else:
                        streak_detector += 1
                        score += len(mot_actuel)
                    return demarrer_jeu()
                elif event.key == pygame.K_RETURN and saisie_utilisateur != mot_actuel:
                    pygame.display.update()
                    if streak > mstreak:
                        mstreak = streak
                    streak = 0
                    streak_detector = 0
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
    fenetre.blit(image, (0, 700))


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


def get_best_score():
    f = open("scores/bestScore.sc", "r+")
    not_cleaned_old = f.read()
    old = not_cleaned_old.strip('\x00')
    if old:
        return int(old)
    return 0


def get_last_score():
    f = open("scores/lastScore.sc", "r+")
    not_cleaned_old = f.read()
    old = not_cleaned_old.strip('\x00')
    if old:
        return int(old)
    return 0


def write_best_score(points):
    f = open("scores/bestScore.sc", "r+")
    not_cleaned_old = f.read()
    old = not_cleaned_old.strip('\x00')
    if old and points > int(old):
        f.truncate(0)
        f.write(str(points))
    elif not old:
        f.truncate(0)
        f.write(str(points))
    f.close()


def write_last_score(points):
    f = open("scores/lastScore.sc", "w")
    f.truncate(0)
    f.write(str(points))
    f.close()


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
