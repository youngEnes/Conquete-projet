import random
import pygame
import time
from time import sleep
import pandas
"""
La tête du code !!!
"""
# Initialisation de Pygame avec nos constantes
pygame.init()
TAILLE_CASE = 60 #taille de chaque case pour le jeu 
MARGE = 5 #marge entre les case pour faire comme une grille
LARGEUR, HAUTEUR = 1920, 1080
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.mixer.init(frequency=44100, size=-16, channels=2)
pygame.font.init()
font = pygame.font.Font('modules/modules2/Retro Gaming.ttf', 36)

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

#Chargement des sons made by firass le goat
son_menu=pygame.mixer.Sound("modules/modules2/Musique de fond pour le menu.wav")
son_changement_selection=pygame.mixer.Sound("modules/modules2/Changement de sélection dans le menu.wav")
son_jeu = pygame.mixer.Sound("modules\modules2\modules3\Musique de fond lorsqu'on est en pleine partie.wav")
son_victoire = pygame.mixer.Sound("modules\modules2\modules3\Gagné.wav")
son_defaite = pygame.mixer.Sound("modules\modules2\modules3\Perdu.wav")
son_clic = pygame.mixer.Sound("modules\modules2\modules3\Bruit lorsque tu cliques.wav")

# Constantes pour la génération de la grille
TAILLE_CASE = 50
MARGE = 5

#nom des bouton pour le menu
boutton1="Jouer"
boutton2="Quitter"

#Fonctions sonores
def jouer_boucle(son):
    pygame.mixer.stop()
    son.play(loops=-1)
def jouer_son_unique(son):
    pygame.mixer.stop()
    son.play()
# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("None")#aucun titre pour cette fenêtre : c'est pour ça qu'il y a "None"

#les fct qui permettent d'afficher les éléments sur notre meeeerveilleux écran de menu ! lol
def afficher_texte(fenetre, texte, position, taille=30, couleur=NOIR):
    """ Affiche un texte à l'écran """
    police = pygame.font.Font('modules/modules2/Retro Gaming.ttf', taille)
    rendu = police.render(texte, True, couleur)
    fenetre.blit(rendu, position)
def afficher_bouton(fenetre, texte, rect, couleur_fond, couleur_texte):
    """
    Affiche un bouton interactif pour le menu nottamment
    """
    pygame.draw.rect(fenetre, couleur_fond, rect)
    afficher_texte(fenetre, texte, (rect[0] + 20, rect[1] + 10), 40, couleur_texte)

"""
Corps du texte
"""
#fct pour le fonctionnement de notre grille, je vais te griller mec !
def generation(n: int, N: int) -> list:
    """
    fonction qui permet de générer de manière aléatoire le contenu de la liste grille avec n ligne et collone et N nombre
    """
    assert type(n) == int, "n doit être un entier"
    assert type(N) == int, "N doit être un entier"
    assert n in [2, 6, 10, 14], "n doit être 2, 6, 10 ou 14"
    assert 4 <= N <= 7, "N doit être entre 4 et 7"
    grille = [[random.randint(0, N) for _ in range(n)] for _ in range(n)]
    #postconditions:
    assert type(grille)==list,"cela doit être une liste "
    return grille
#Jeux de test
generation(2,5)==[[2,5],[5,6]]
generation(6,7)==[[1,5,6,3,2,3],[5,3,2,7,4,1],[3,1,6,4,7,2],[1,3,4,5,6,2],[2,4,3,7,1,2],[2,3,2,4,5,5]]

def propagation(grille:list, x:int, y:int) -> list:
    """
    fonction qui permet de propager
    """
    n = len(grille)
    ancien = grille[0][0]
    nouveau = grille[x][y]
    if ancien == nouveau: #si la case 00 et la case selectionnée sont égales cela revient à la même chose donc cela ne fait rien
        return grille
    à_visiter = [(0, 0)]
    visités = []
    while à_visiter:
        i, j = à_visiter.pop()
        if (i, j) in visités:
            continue  #pour pas que l'on regarde les cases déjà vus
        if grille[i][j] == ancien:
            grille[i][j] = nouveau
            visités.append((i, j))
             # regarde les cases adjacentes
            if i > 0:
                à_visiter.append((i - 1, j))
            if i < n - 1:
                à_visiter.append((i + 1, j))
            if j > 0:
                à_visiter.append((i, j - 1))
            if j < n - 1:
                à_visiter.append((i, j + 1))
    #postconditions 
    assert type(grille)==list ,"cela doit être une liste "
    return grille #retourne la grille modifier
#Jeux de test
propagation([[1,5,6,3,2,3],[5,3,2,7,4,1],[3,1,6,4,7,2],[1,3,4,5,6,2],[2,4,3,7,1,2],[2,3,2,4,5,5]], 5,2)==[[1,5,6,3,2,3],[5,3,2,7,4,1],[3,1,6,4,7,1],[1,3,4,5,6,1],[2,4,3,7,1,1],[2,3,2,4,5,5]]
propagation([[2,5],[2,6]], 0,1)==[[2,5],[2,6]]

def affichergrille(grille: list, fenetre):
    """
    Fct qui permet d'afficher notre magnific grile !
    """
    #préconditions
    assert type(grille)==list , "grille doit être une liste"
    fenetre.fill((0, 102, 204))  # Fond bleuté car on fait fenetre.fill((nuancerouge,nuancevert,nuance bleu))
    font = pygame.font.Font(None, 36)
    n = len(grille)
    largeurgrille = n * TAILLE_CASE + (n - 1) * MARGE
    longueurgrille = n * TAILLE_CASE + (n - 1) * MARGE
    # Calcul du décalage  pour centrer la grille
    décalagehorizontale = (fenetre.get_width()-largeurgrille)//2 #get width permet de récupérerla largeur de la grille
    décalageverticale = (fenetre.get_height()-longueurgrille)//2 #get heght permet de récupérer la hauteur de la grille
    # Dessiner les cases de la grille
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            rect = pygame.Rect(décalagehorizontale + j * (TAILLE_CASE + MARGE), décalageverticale + i * (TAILLE_CASE + MARGE),TAILLE_CASE, TAILLE_CASE   )
            pygame.draw.rect(fenetre, (200, 200, 200), rect)  # Dessiner le fond de la case
            pygame.draw.rect(fenetre, (0, 0, 0), rect, 2)     # Dessiner le contour de la case
            # Dessiner le texte à l'intérieur de la case
            texte = font.render(str(grille[i][j]), True, (0, 0, 0))
            texte_rect = texte.get_rect(center=rect.center)
            fenetre.blit(texte, texte_rect)
    pygame.display.flip()  # Mettre à jour l'affichage, jaaj !
#définition variable comme cela on peut la mettre en global
limite=0
coups=0
#boucle jouer qui permet de vraiment lancer le jeu
def jouer(n: int, N: int):
    """
    Boucle de jeu de base qui permet de jouer au jeu de conquete
    """
    #préconditions
    assert type(n)==int ,"n doit être un entier"
    assert type(N)==int,"N doit être un entier"
    global limite,coups
    pygame.init()
    essais = {2: 4, 6: 14, 10: 24, 14: 34}
    limite = essais[n]
    coups = 0
    taille_fenetre = n * TAILLE_CASE + (n - 1) * MARGE
    fenetre = pygame.display.set_mode((taille_fenetre, taille_fenetre))
    pygame.display.set_caption("Napoléon conquest") #cela permet de changer le titre de la fenêtre pygame

    icone = pygame.image.load("napoleon.jpeg")#mise en place de l'îcone
    pygame.display.set_icon(icone)#permet de mettre l'icône
    grille = generation(n, N)
    affichergrille(grille, fenetre)
    jouer_boucle(son_jeu) #mets la musique
    running = True #activation de la boucle car elle va tourner indéfinement jusqu'à ce qu'il y ait un évenement !
    while running and coups < limite:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:#Detection du clic de la souris
                x, y = event.pos
                i = y//(TAILLE_CASE + MARGE)
                j = x//(TAILLE_CASE + MARGE)
                if 0 <=i< n and 0 <=j<n:
                    propagation(grille, i, j)
                    affichergrille(grille, fenetre)
                    coups += 1
                    print(f"Il te reste {limite - coups} essais.")
                    if all(case == grille[0][0] for row in grille for case in row):#Vérifie si toutes les cases sont égales à l'origine->t'as gagné masterclasse !!!!
                        pygame.mixer.stop()
                        sleep(1)
                        jouer_son_unique(son_victoire)
                        print(f"🎉 Bravo, tu as gagné en {coups} coups !")
                        sleep(2)
                        pygame.quit()
                        return
    if not all(case == grille[0][0] for row in grille for case in row): #si pas les toutes cases sont égales à l'origine ça veut dire que t'as perdu gros looser !!
        jouer_son_unique(son_defaite)
        print("💥 Perdu ! Tu as utilisé tous tes essais. Essaye encore gros naze!")
        sleep(2)
        pygame.quit()
        return
    sleep(1)
    jouer_son_unique(son_defaite)
    pygame.quit()
    print("💥 Perdu ! Tu as utilisé tout tes essais loser")
    print("La prochaine fois tu joueras mieux lol xD")
    print("Bravo ta stratégie est aussi efficace qu'un ordinateur avec 256 Mo de ram lol")
def choisir_N(): #fonction pour le choix de grand N
    """
     Menu graphique pour sélectionner la valeur de n
     """
    running = True #activation de la boucle car elle va tourner indéfinement jusqu'à ce qu'il y ait un évenement !
    jouer_boucle(son_menu)
    # Charger les images de notre GIF en arrière plan qui est tellement masterclasse !!
    clock = pygame.time.Clock()
    frame_index = 0
    frames = [pygame.image.load(f"modules/modules2/frame_{i}.png") for i in range(0, 107)] #création d'une liste contenat toutes les frmes du gif puis les affcihe un par un en arrière plan
    valeurs_N = [4, 5, 6, 7]
    boutons = [pygame.Rect(150, 200 + i * 80, 500, 60) for i in range(len(valeurs_N))] #crée un boutton avec les valeurs de N
    while running:
        fenetre.fill((0,0,0))
        fenetre.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % len(frames)
        clock.tick(10)
        afficher_texte(fenetre, "Choisis le chiffre N maximum dans le tableau ", (200, 100), 50, BLANC)
        for i, bouton in enumerate(boutons):
            afficher_bouton(fenetre, f"N= {valeurs_N[i]}", bouton, NOIR, BLANC)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, bouton in enumerate(boutons):
                    if bouton.collidepoint(x, y):
                        running = False
                        pygame.mixer.stop()
                        jouer_son_unique(son_changement_selection)
                        sleep(0.5)
                        N=valeurs_N[i]
                        pygame.quit()
                        return N  # Retourne la valeur sélectionnée
def choisir_n():
    """
     Menu graphique pour sélectionner la valeur de n
     """
    running = True #activation de la boucle car elle va tourner indéfinement jusqu'à ce qu'il y ait un évenement !
    jouer_boucle(son_menu)
    # Charger les images de notre GIF en arrière plan qui est tellement masterclasse !!
    clock = pygame.time.Clock()
    frame_index = 0
    frames = [pygame.image.load(f"modules/modules2/frame_{i}.png") for i in range(0, 107)]
    valeurs_n = [2, 6, 10, 14]
    boutons = [pygame.Rect(150, 200 + i * 80, 500, 60) for i in range(len(valeurs_n))]
    while running:
        fenetre.fill((0,0,0))
        fenetre.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % len(frames)
        clock.tick(10)#vitesse d'animation
        afficher_texte(fenetre, "Choisi la taille de la grille (n=nb de carreaux par côté)", (200, 100), 50, BLANC)
        for i, bouton in enumerate(boutons):
            afficher_bouton(fenetre, f"n = {valeurs_n[i]}", bouton, NOIR, BLANC)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, bouton in enumerate(boutons):
                    if bouton.collidepoint(x, y): #renvoie true quand la souris est dans le rectange x y 
                        running = False
                        pygame.mixer.stop()
                        jouer_son_unique(son_changement_selection) #mets le son de changement quand il ya un clic
                        sleep(0.5)
                        n=valeurs_n[i]
                        return n  # Retourne la valeur sélectionnée
def score_csv ():
    """
    Fonction qui permet de stocker en csv 
    """
    global limite,coups
    nom_utilisateur=str(input("Entre un nom d'utilisateur giga chad, bro !"))#entre ton nom d'utilisateur, j'espère qu'il sera masterclasse !!!
    score_csv=pandas.read_csv("affichage des scores.csv")#On charge le fichier csv qui permet de determiner son score
    score_jeu=(limite-coups)*1000 #Le score
    print(nom_utilisateur,score_jeu)
    enregistrement_des_donnees={"Pseudo": nom_utilisateur, "Nb de points" : score_jeu}
    score_csv=pandas.concat([score_csv, pandas.DataFrame([enregistrement_des_donnees])], ignore_index=True)
    score_csv.to_csv("affichage des scores.csv", index=False)
    print(score_csv)

def menu():
    """
    Affiche un menu graphique avec boutons interactifs
    """
    pygame.display.set_caption("Conquête - Menu Principal")
    sleep(0.5)
    running = True
    jouer_boucle(son_menu)
    # Charger les images de notre GIF en arrière plan qui est tellement masterclasse !!
    clock = pygame.time.Clock()
    frames = [pygame.image.load(f"modules/modules2/frame_{i}.png") for i in range(0, 107)]
    frame_index = 0
    while running:
        fenetre.fill((0,0,0))
        fenetre.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % len(frames)
        clock.tick(10)
        afficher_texte(fenetre, "Jeu de Conquête", (250, 100), 50, BLANC)
        # Définition des boutons
        bouton_jouer = pygame.Rect(540, 300, 500, 60)
        bouton_quitter = pygame.Rect(540, 400, 500, 60)
        afficher_bouton(fenetre, boutton1, bouton_jouer, NOIR, BLANC)
        afficher_bouton(fenetre, boutton2, bouton_quitter, NOIR, BLANC)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if bouton_jouer.collidepoint(x, y): #si le boutton est cliqué
                    running = False
                    pygame.mixer.stop()
                    jouer_son_unique(son_changement_selection)
                    sleep(0.5)
                    n=choisir_n()
                    N=choisir_N()
                    jouer(n,N)
                    sleep(1)
                    score_csv()
                elif bouton_quitter.collidepoint(x, y):
                    jouer_son_unique(son_changement_selection)
                    sleep(0.5) #attente de 0.5s : on a tous le droit à une petite pause, n'est-ce pas ?
                    pygame.quit() #quitte pygame si la personne clique sur quitter
menu() #permet de jouer au jeu

