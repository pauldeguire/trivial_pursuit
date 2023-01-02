# -*- coding: utf-8 -*-

from tkinter import Tk, Canvas, messagebox
import pipopipette.partie
import pipopipette.exceptions
import pipopipette.planche


class CanvasPipopipette(Canvas):
    def __init__(self, parent, planche, longueur_ligne=200):
        self.longueur_ligne = longueur_ligne
        self.largeur_ligne = self.longueur_ligne / 5
        self.dimension_boite = self.longueur_ligne + self.largeur_ligne
        self.planche = planche

        super().__init__(parent,
                         width=self.planche.N_BOITES_V * self.dimension_boite + self.largeur_ligne - 1,
                         height=self.planche.N_BOITES_H * self.dimension_boite + self.largeur_ligne - 1)

    def dessiner_boites(self):
        for position, boite in self.planche.boites.items():
            ligne, col = position

            debut_boite_x = col * self.dimension_boite + self.largeur_ligne
            debut_boite_y = ligne * self.dimension_boite + self.largeur_ligne
            fin_boite_x = debut_boite_x + self.longueur_ligne
            fin_boite_y = debut_boite_y + self.longueur_ligne

            self.create_rectangle(debut_boite_x, debut_boite_y, fin_boite_x, fin_boite_y, tags='boite', fill=boite.couleur_affichage())

    def dessiner_lignes(self):
        for cle, ligne in self.planche.lignes.items():
            ligne_point, col_point, orientation = cle

            if orientation == 'H':
                debut_ligne_x = col_point * self.dimension_boite + self.largeur_ligne
                debut_ligne_y = ligne_point * self.dimension_boite
                fin_ligne_x = debut_ligne_x + self.longueur_ligne
                fin_ligne_y = debut_ligne_y + self.largeur_ligne
            else:
                debut_ligne_x = col_point * self.dimension_boite
                debut_ligne_y = ligne_point * self.dimension_boite + self.largeur_ligne
                fin_ligne_x = debut_ligne_x + self.largeur_ligne
                fin_ligne_y = debut_ligne_y + self.longueur_ligne

            self.create_rectangle(debut_ligne_x,
                                  debut_ligne_y,
                                  fin_ligne_x,
                                  fin_ligne_y,
                                  tags='ligne',
                                  fill=ligne.couleur_affichage(),
                                  width=1)

    def dessiner_points(self):
        for col in range(self.planche.N_BOITES_V + 1):
            for ligne in range(self.planche.N_BOITES_H + 1):
                origine_cercle_x = col * self.dimension_boite
                origine_cercle_y = ligne * self.dimension_boite
                fin_cercle_x = origine_cercle_x + self.largeur_ligne
                fin_cercle_y = origine_cercle_y + self.largeur_ligne

                self.create_oval(origine_cercle_x,
                                 origine_cercle_y,
                                 fin_cercle_x,
                                 fin_cercle_y,
                                 tags='point',
                                 fill='black')

    def obtenir_coup_joue(self, event):
        '''
        Méthode qui retrouve si un clic est fait sur une ligne, une boîte ou sur un point, et surtout pour retrouver
        laquelle.

        Dans votre TP, vous pourrez vous débarasser des sections de code concernant les clics sur un
        point et sur une boîte pour conserver seulement les sections sur les lignes et retourner None
        quand le clic est sur un point ou une boîte.

        Args:
            event (Event): L'objet Event relié au clic fait sur le canvas

        Returns:
            None si le clic a été fait sur un point, (int, int, orientation) s'il
            a été fait sur une ligne et (int, int, 'Boite') si c'était une boîte
        '''
        col = int(event.x // self.dimension_boite)
        ligne = int(event.y // self.dimension_boite)

        x_relatif = event.x % self.dimension_boite
        y_relatif = event.y % self.dimension_boite

        coup = None

        if x_relatif < self.largeur_ligne:
            if y_relatif > self.largeur_ligne:
                # Clic sur une ligne verticale
                coup = (ligne, col, 'V')

        else:
            if y_relatif < self.largeur_ligne:
                # Clic sur une ligne horizontale
                coup = (ligne, col, 'H')

        return coup

    def actualiser(self):
        # On supprime les anciennes boîtes et on ajoute les nouvelles.
        self.delete('boite')
        self.dessiner_boites()

        # On supprime les anciennes lignes et on ajoute les nouvelles.
        self.delete('ligne')
        self.dessiner_lignes()

        # On dessine les points
        self.dessiner_points()


class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        self.resizable(0, 0)

        self.title('Pipopipette')

        self.partie = pipopipette.partie.PartiePipopipette()

        self.initialiser_canvas()

        self.canvas_planche.bind('<Button-1>', self.selectionner)

    def initialiser_canvas(self):
        self.canvas_planche = CanvasPipopipette(self, self.partie.planche)
        self.canvas_planche.actualiser()
        self.canvas_planche.grid()

    def selectionner(self, event):
        '''
        Dans votre TP, le retour de obtenir_coup_joue() sera à None si et seulement si le clic
        N'a PAS été effectué une ligne. Ainsi, si le coup est None, on ne fera rien, sinon on le jouera
        avec self.partie.jouer_coup(). Aussi, si le coup est sur une ligne déjà jouée, on attrapera
        l'exception lancée dans Planche.valider_coup() et on affichera un message d'erreur correspondant.
        Enfin, on s'assurera aussi de faire appel à l'actualisation du canvas et à la logique de
        fin de partie.

        Args:
            event (Event): L'objet Event relié au clic fait sur le canvas
        '''
        coup = self.canvas_planche.obtenir_coup_joue(event)

        if coup is not None:
            self.partie.jouer_coup(coup)

        self.canvas_planche.actualiser()

        if self.partie.partie_terminee():
            messagebox.showinfo("Partie terminée",f"Le joueur {self.partie.gagnant_partie} a gagné la partie!")
            if messagebox.askyesno('Nouvelle partie', 'Voulez-vous jouer une nouvelle partie?'):
                self.partie = pipopipette.partie.PartiePipopipette()
                self.canvas_planche.planche = self.partie.planche
                self.canvas_planche.actualiser()
            else:
                self.destroy()
