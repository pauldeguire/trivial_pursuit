# -*- coding: utf-8 -*-

import random


class Joueur:
    '''
    Classe générale de joueur. Vous est fournie.
    '''

    def __init__(self, couleur):
        '''
        Le constructeur global de Joueur.

        Args :
            couleur (str): la couleur qui sera jouée par le joueur.
        '''
        assert couleur in ["bleu", "rouge"], "Piece: couleur invalide."

        self.couleur = couleur

    def obtenir_type_joueur(self):
        '''
        Cette méthode sera implémentée par JoueurHumain et JoueurOrdinateur

        Returns :
            'Ordinateur' ou 'Humain'
        '''
        pass

    def choisir_coup(self, planche):
        '''
        Cette méthode sera implémentée par JoueurHumain et JoueurOrdinateur.

        Args :
            planche (Plache): la planche sur laquelle le joueur choisit son coup

        Returns:
            (int, int, str): L'index du la ligne (le coup) choisi par le joueur.
        '''
        pass


class JoueurHumain(Joueur):
    '''
    Classe modélisant un joueur humain.
    '''

    def __init__(self, couleur):
        '''
        Cette méthode va construire un objet Joueur et
        l'initialiser avec la bonne couleur.
        '''
        super().__init__(couleur)

    def obtenir_type_joueur(self):
        return "Humain"

    def choisir_coup(self, planche):
        '''
        Demande à l'usager quel coup il désire jouer. Comme un coup est
        constitué d'une ligne, d'une colonne et d'une orientation, on doit
        demander chacune des trois valeurs à l'usager.

        On retourne ensuite l'ndex correspondant aux trois valeurs dans l'ordre
        (ligne, colonne, orientation).

        Args :
            planche (Plache): la planche sur laquelle le joueur choisit son coup

        Returns:
            (int, int, str): L'index du la ligne (le coup) choisi par le joueur.
        '''
        ligne = int(input("Quel est l'index de la ligne du coup que vous désirez jouer? "))
        col = int(input("Quel est l'index de la colonne du coup que vous désirez jouer? "))
        orientation = input("Quelle est l'orientation du coup vous désirez jouer? ")

        return ligne, col, orientation


class JoueurOrdinateur(Joueur):
    '''
    Classe modélisant un joueur ordinateur.
    '''

    def __init__(self, couleur):
        '''
        Cette méthode va construire un objet Joueur et
        l'initialiser avec la bonne couleur.
        '''
        super().__init__(couleur)

    def obtenir_type_joueur(self):
        return "Ordinateur"

    def choisir_coup(self, planche):
        '''
        Méthode qui va choisir aléatoirement un coup parmi les
        coups possibles sur la planche. Pensez à utiliser
        random.choice() et planche.obtenir_coups_possibles() pour
        vous faciliter la tâche.

        N.B. Vous pouvez sans aucun problème implémenter un
                joueur ordinateur plus avancé qu'un simple choix
                aléatoire. Il s'agit seulement du niveau minimum requis.

        Args :
            planche (Plache): la planche sur laquelle le joueur choisit son coup

        Returns:
            (int, int, str): L'index du la ligne (le coup) choisi par le joueur.
        '''
        return random.choice(planche.obtenir_coups_possibles())
