# encoding=latin_1
import os, sys
import random
import time
import traceback

'''#==========# EXEMPLE #==========#
I\J  0   1   2   3   4   5   6   7
   ┌───┬───┬───┬───┬───┬───┬───┬───┐
 0 │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │
   ├───┼───┼───┼───┼───┼───┼───┼───┤
 1 │ 0 │ 0 │[3]│ 0 │ 0 │ 0 │ 0 │ 0 │
   ├───┼───┼───┼───┼───┼───┼───┼───┤
 2 │ 0 │ 0 │[3]│ 0 │ 0 │ 0 │ 0 │ 0 │
   ├───┼───┼───┼───┼───┼───┼───┼───┤
 3 │ 0 │ 0 │[3]│ 0 │ 0 │ 0 │ 0 │ 0 │
   ├───┼───┼───┼───┼───┼───┼───┼───┤
 4 │ 0 │ 0 │ 0 │[3]│[3]│[3]│ 0 │ 0 │
   ├───┼───┼───┼───┼───┼───┼───┼───┤
 5 │ 0 │[2]│ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │
   ├───┼───┼───┼───┼───┼───┼───┼───┤
 6 │ 0 │[2]│ 0 │[4]│[4]│[4]│[4]│ 0 │
   ├───┼───┼───┼───┼───┼───┼───┼───┤
 7 │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │ 0 │
   └───┴───┴───┴───┴───┴───┴───┴───┘
'''

def clear(): #Fonction juste pour facilement effacer la console et avoir un affichage propre
    os.system('cls' if os.name=='nt' else 'clear')

def affichageGrille(Grille, mode):
    ##########################################
    # Affichage de la Grille 8x8 en argument #
    ##########################################

    ligne = ""
    
    if mode == 1: #Mode qui permet de voir les navires de la grille (voir ses propres navires)
        print("     0   1   2   3   4   5   6   7")
        print("   |---+---+---+---+---+---+---+---|")
        for i in range(8):
            for j in range(8):
                if Grille[i][j] == 0: #Zone vide
                    ligne = ligne + "|   "
                elif Grille[i][j] == 5: #Zone vide déjà touchée
                    ligne = ligne + "| X "
                elif Grille[i][j] >= 6: #Partie de navire déjà touchée
                    ligne = ligne + "|[X]"
                else: #Partie de navire
                    ligne = ligne + "|[" + str(Grille[i][j]) + "]"
            ligne = " " + str(i) + " " + ligne + "|"
            print(ligne)
            if i < 8:
                print("   |---+---+---+---+---+---+---+---|")
            ligne = ""
    else: #Mode avec navires non révélés (brouillard de guerre)
        print("     0   1   2   3   4   5   6   7")
        print("   |---+---+---+---+---+---+---+---|")
        for i in range(8):
            for j in range(8):
                if Grille[i][j] == 0:
                    ligne = ligne + "|   "
                elif Grille[i][j] == 5:
                    ligne = ligne + "| X "
                elif Grille[i][j] >= 6:
                    ligne = ligne + "|[X]"
                else:
                    ligne = ligne + "|   "
            ligne = " " + str(i) + " " + ligne + "|"
            print(ligne)
            if i < 8:
                print("   |---+---+---+---+---+---+---+---|")
            ligne = ""

def generateBotGrid(): #Génération de la grille de l'ordinateur
    GrilleOrdi = [[0] * 8 for z in range(8)] #Grille de l'ordinateur
    
    for nombreNavires in range(4):
        if nombreNavires == 0:
            tailleNavire = 2
        elif nombreNavires == 3:
            tailleNavire = 4
        else:
            tailleNavire = 3
        pos_i = random.randint(0,7) #Lignes (Haut vers le bas)
        pos_j = random.randint(0,7) #Colonnes (Gauche vers la droite)
        direction = random.randint(0,3) #Direction de pose des navires
        ok = 0 #Clé pour rester dans la boucle si il a un problème avec le placement
        while ok == 0: #Tant qu'un navire n'a pas réussi à être placé, cette boucle continue
            if (direction == 0) and (pos_j + tailleNavire < 8): #Droite : Test pour empêcher de poser un navire en dehors de la grille
                ok = 1
                for x in range(tailleNavire): #Test pour être sûr de ne pas poser un navire sur un autre navire
                    if GrilleOrdi[pos_i][pos_j+x] != 0:
                        ok = 0 #Si un navire déjà existant gêne, on perd la clé et on reste dans la boucle avec de nouvelles valeurs aléatoires
                if ok == 1:
                    for x in range(tailleNavire): #Boucle pour poser le navire
                        GrilleOrdi[pos_i][pos_j+x] = nombreNavires + 1
            elif (direction == 1) and (pos_i + tailleNavire < 8): #Bas
                ok = 1
                for x in range(tailleNavire):
                    if GrilleOrdi[pos_i+x][pos_j] != 0:
                        ok = 0
                if ok == 1:
                    for x in range(tailleNavire):
                        GrilleOrdi[pos_i+x][pos_j] = nombreNavires + 1
            elif (direction == 2) and (pos_j - tailleNavire >= 0): #Gauche
                ok = 1
                for x in range(tailleNavire):
                    if GrilleOrdi[pos_i][pos_j-x] != 0:
                        ok = 0
                if ok == 1:     
                    for x in range(tailleNavire):
                        GrilleOrdi[pos_i][pos_j-x] = nombreNavires + 1
            elif (direction == 3) and (pos_i - tailleNavire >= 0): #Haut
                ok = 1
                for x in range(tailleNavire):
                    if GrilleOrdi[pos_i-x][pos_j] != 0:
                        ok = 0
                if ok == 1:
                    for x in range(tailleNavire):
                        GrilleOrdi[pos_i-x][pos_j] = nombreNavires + 1
            if ok == 0:
                direction = random.randint(0,3)
                pos_i = random.randint(0,7)
                pos_j = random.randint(0,7)
                
    affichageGrille(GrilleOrdi, 1)
    return(GrilleOrdi)

def createPlayerGrid(): #Fabrication de la grille de joueur
    GrilleJoueur = [[0] * 8 for z in range(8)]
    PtsPossible = [[0] * 2 for y in range(4)]
    for nombreNavires in range(4):
        clear()
        affichageGrille(GrilleJoueur, 1)
        if nombreNavires == 0:
            tailleNavire = 2
        elif nombreNavires == 3:
            tailleNavire = 4
        else:
            tailleNavire = 3
        ok = 0
        while ok == 0: #Tant que l'on a pas mis un navire à une position acceptable
            try:
                input_J = int(input("\nChoix du premier point d'ancrage du navire de taille " + str(tailleNavire) + "\nColonne (0 -> 7) : "))
                nbrChoix = 0
                if input_J < 0 or input_J > 7:
                    print("\nChoix invalide ! (0 -> 7)")
                else:
                    try: #On fait choisir un premier point avec X/Y puis on détermine les coordonnées possibles du deuxième point (minimum 2 | maximum 4)
                        input_I = int(input("Ligne (0 -> 7) : "))
                        if input_I < 0 or input_I > 7:
                            print("\nChoix invalide ! (0 -> 7)")
                        else:
                            print("\nChoix possibles :")
                            if (input_J + (tailleNavire - 1)) < 8:
                                PtsPossible[nbrChoix][0] = input_I
                                PtsPossible[nbrChoix][1] = (input_J + (tailleNavire - 1))
                                nbrChoix += 1
                            if (input_I + (tailleNavire - 1)) < 8:
                                PtsPossible[nbrChoix][0] = (input_I + (tailleNavire - 1))
                                PtsPossible[nbrChoix][1] = input_J
                                nbrChoix += 1
                            if (input_J - (tailleNavire - 1)) >= 0:
                                PtsPossible[nbrChoix][0] = input_I
                                PtsPossible[nbrChoix][1] = (input_J - (tailleNavire - 1))
                                nbrChoix += 1
                            if (input_I - (tailleNavire - 1)) >= 0:
                                PtsPossible[nbrChoix][0] = (input_I - (tailleNavire - 1))
                                PtsPossible[nbrChoix][1] = input_J
                                nbrChoix += 1
                            for x in range(nbrChoix):
                                print(str(x + 1) + ") (" + str(PtsPossible[x][1]) + "," + str(PtsPossible[x][0]) + ")")
                            try: #On fait choisir à l'utilisateur l'un des points calculés à partir du premier
                                inputUtilisateur = int(input("\n: "))
                                if inputUtilisateur < 1 or inputUtilisateur > nbrChoix:
                                    print("\nChoix invalide ! (1 -> " + str(nbrChoix) + ")")
                                    continue
                                else: # Placement sur grille avec conditions
                                    inputUtilisateur -= 1
                                    ok = 1
                                    if PtsPossible[inputUtilisateur][1] == input_J:
                                        for x1 in range(tailleNavire): #Check si pas d'obstacle là où on veut placer le navire
                                            if PtsPossible[inputUtilisateur][0] > input_I:
                                                if GrilleJoueur[input_I + x1][input_J] != 0:
                                                    ok = 0
                                            else:
                                                if GrilleJoueur[input_I - x1][input_J] != 0:
                                                    ok = 0
                                        if ok == 1:
                                            for x1 in range(tailleNavire): #On place le navire
                                                if PtsPossible[inputUtilisateur][0] > input_I:
                                                    GrilleJoueur[input_I + x1][input_J] = nombreNavires + 1
                                                else:
                                                    GrilleJoueur[input_I - x1][input_J] = nombreNavires + 1
                                    else:
                                        for x2 in range(tailleNavire):
                                            if PtsPossible[inputUtilisateur][1] > input_J:
                                                if GrilleJoueur[input_I][input_J + x2] != 0:
                                                    ok = 0
                                            else:
                                                if GrilleJoueur[input_I][input_J - x2] != 0:
                                                    ok = 0
                                        if ok == 1:
                                            for x2 in range(tailleNavire):
                                                if PtsPossible[inputUtilisateur][1] > input_J:
                                                    GrilleJoueur[input_I][input_J + x2] = nombreNavires + 1
                                                else:
                                                    GrilleJoueur[input_I][input_J - x2] = nombreNavires + 1
                                if ok == 0:
                                    print("\nImpossible a placer, un autre navire est deja present !\n")
                                    continue
                            except:
                                print("Choix inexistant, recommencez avec un nombre entre 1 et " + str(nbrChoix) + " (compris).")
                                continue
                    except:
                        print("Choix inexistant, recommencez avec un nombre entre 0 et 7 (compris).")
                        continue
            except:
                print("Choix inexistant, recommencez avec un nombre entre 0 et 7 (compris).")
                continue
    return(GrilleJoueur)

def playerPlay(GrilleOrdi): #Fonction pour faire jouer le joueur Humain
    ok = 0
    testDetruit = 0
    while ok == 0:
        try:
            input_J = int(input("\nColonne (0 -> 7) : "))
            if input_J < 0 or input_J > 7:
                print("Choix invalide ! (0 -> 7)")
                continue
            else:
                try:
                    input_I = int(input("Ligne (0 -> 7) : "))
                    if input_J < 0 or input_J > 7:
                        print("Choix invalide ! (0 -> 7)")
                        continue
                    else:
                        if GrilleOrdi[input_I][input_J] == 0: #Dans l'eau, raté
                            clear()
                            print("\n\tTir manque !\n\n")
                            GrilleOrdi[input_I][input_J] = 5
                            ok = 1
                        elif GrilleOrdi[input_I][input_J] >= 1 and GrilleOrdi[input_I][input_J] <= 4: #Bateau touché
                            clear()
                            print("\n\tTouche !")
                            idNavire = GrilleOrdi[input_I][input_J]
                            GrilleOrdi[input_I][input_J] = idNavire + 5
                            ok = 1
                            testDetruit = 1
                            for i in range(8): #Test pour afficher si u navire a été coulé et quel tye de navire est-ce.
                                for j in range(8):
                                    if GrilleOrdi[i][j] == idNavire:
                                        testDetruit = 0
                            if testDetruit == 1: #Si pas d'autres case du même bateau dansla grille
                                if idNavire == 1:
                                    print("    Vous avez detruit le contre-torpilleur !\n") #2 cases
                                elif idNavire == 2:
                                    print("    Vous avez detruit le croiseur !\n") #3 cases
                                elif idNavire == 3:
                                    print("    Vous avez detruit le sous-marin !\n") #3 cases
                                else:
                                    print("    Vous avez detruit le porte-avions !\n") #4 cases
                            else:
                                print("\n")
                        elif GrilleOrdi[input_I][input_J] == 5: #Dans l'eau, déjà tiré ici
                            print("Vous avez deja fait feu sur cette case...")
                            continue
                        else: #Zone de bateau déjà touché
                            print("Vous avez deja fait feu sur cette partie du navire...")
                            continue
                except:
                    print("Choix inexistant, recommencez avec un nombre entre 0 et 7 (compris).")
                    continue
        except:
            print("Choix inexistant, recommencez avec un nombre entre 0 et 7 (compris).")
            continue
            
    return(GrilleOrdi)

def botPlay(Grille):
    ok = 0
    while ok == 0: #Boucle pour empêcher le bot de jouer un coup à un endroit déjà tenté
        ok = 1
        pos_i = random.randint(0,7)
        pos_j = random.randint(0,7)
        if Grille[pos_i][pos_j] >= 5:
            ok = 0
        elif Grille[pos_i][pos_j] == 0:
            Grille[pos_i][pos_j] = 5
        else:
            idNavire = Grille[pos_i][pos_j]
            Grille[pos_i][pos_j] = idNavire + 5
    return(Grille)

def finDeJeu(Grille): #Check fin de parties
    gameOver = 1
    for i in range(8):
        for j in range(8):
            if Grille[i][j] >= 1 and Grille[i][j] <= 4:
                gameOver = 0
    return(gameOver)
            

def gameLoop(mode): #Boucle de jeu
    if mode == 1:
        GrilleOrdi = [[0] * 8 for z in range(8)] #Grille de l'ordinateur
        GrilleOrdi = generateBotGrid()
        print("\nGrille de l'ordinateur generee.\n\nCreation de la grille du joueur :")
        GrilleJoueur_1 = [[0] * 8 for z in range(8)] #Grille du joueur (joueur 1 si JCJ)
        GrilleJoueur_1 = createPlayerGrid()
    else:
        print("\nCreation de la grille du joueur 1 :\n")
        GrilleJoueur_1 = [[0] * 8 for z in range(8)] #Grille du joueur 1
        GrilleJoueur_1 = createPlayerGrid()
        print("\nCreation de la grille du joueur 2 :\n")
        GrilleJoueur_2 = [[0] * 8 for z in range(8)] #Grille du joueur 2
        GrilleJoueur_2 = createPlayerGrid()
    clear()
    print("\n\n\n")
    if mode == 1:
        playerWin = 0
        botWin = 0
        while playerWin == 0 and botWin == 0: #Boucle de jeu, fin lorsque le joueur ou le bot n'a plus de navires.
            affichageGrille(GrilleOrdi, 0) #Affichage de la grille du bot avec brouillard de guerre
            affichageGrille(GrilleJoueur_1, 1) #Affichage de la grille du joueur avec toutes les informations
            GrilleOrdi = playerPlay(GrilleOrdi) #Modification de la grille du bot en fonction du coup joué par le joueur
            playerWin = finDeJeu(GrilleOrdi) #Test pour voir si le joueur a gagné
            GrilleJoueur_1 = botPlay(GrilleJoueur_1) #Modification de la grille du bot en fonction du coup joué par le bot
            botWin = finDeJeu(GrilleJoueur_1) #Test pour voir si le bot a gagné
        if playerWin == 1: #Si le joueur a gagné
            print("\nVous avez remporte la bataille !\n")
        else: #Sinon c'est donc le bot qui a gagné
            print("\nVouz avez perdu !\n")
        affichageGrille(GrilleOrdi, 0)
        affichageGrille(GrilleJoueur_1, 1)
    else:
        player1Win = 0
        player2Win = 0
        while player1Win == 0 and player2Win == 0: #Boucle de jeu, fin lorsque l'un des deux joueurs n'a plus de navires.
            affichageGrille(GrilleJoueur_2, 0) #Affichage de la grille du joueur 2 avec brouillard de guerre
            affichageGrille(GrilleJoueur_1, 1) #Affichage de la grille du joueur 1 avec toutes les informations
            print("   [)=-=-=-=(] Joueur  1 [)=-=-=-=(]")
            GrilleJoueur_2 = playerPlay(GrilleJoueur_2) #Le Joueur 1 joue
            player1Win = finDeJeu(GrilleJoueur_2) #Test pour voir si le joueur 1 a gagné
            if player1Win == 1: #Si le joueur 1 gagne, on ne laisse pas le joueur 2 faire un dernier coup pour rien
                break
            affichageGrille(GrilleJoueur_1, 0) #Affichage de la grille du joueur 1 avec brouillard de guerre
            affichageGrille(GrilleJoueur_2, 1) #Affichage de la grille du joueur 2 avec toutes les informations
            print("   [)=-=-=-=(] Joueur  2 [)=-=-=-=(]")
            GrilleJoueur_1 = playerPlay(GrilleJoueur_1) #Le joueur 2 joue
            player2Win = finDeJeu(GrilleJoueur_1) #Test pour voir si le joueur 2 a gagné
        if player1Win == 1: #Si le joueur 1 a gagné
            print("\nLe joueur 1 a remporte la bataille !\n")
        else: #Sinon c'est donc le joueur 2 qui a gagné
            print("\nLe joueur 2 a remporte la bataille !\n")
        print("\n   [)=-=-=-=(] Joueur  1 [)=-=-=-=(]\n")
        affichageGrille(GrilleJoueur_1, 1)
        print("\n   [)=-=-=-=(] Joueur  2 [)=-=-=-=(]\n")
        affichageGrille(GrilleJoueur_2, 1)
            
def Menu():
    clear()
    try:
        inputUtilisateur = int(input("\n\t/|====//=======\\\====|\\\n\t||===||_/Menu\_ ||===||\n\t\\|====\\\=======//====|/\n\n1) Joueur contre Ordinateur\n2) Joueur contre Joueur\n\nVotre choix : "))
        if inputUtilisateur < 1 or inputUtilisateur > 2: #Je ne sais pas trop si je vais laisser le choix 2...
            print(str(inputUtilisateur) + " est un choix invalide ! (1 ou 2)")
        else:
            clear()
            gameLoop(inputUtilisateur)
    except Exception, e:
        print("Choix inexistant, recommencez. : ")
        traceback.print_exc() #Trace pour localiser des erreurs bien cachées, sinon je vois rien comme debug à cause du try

Menu()
