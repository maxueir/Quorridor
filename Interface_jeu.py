import State
import tkinter as tk
import threading
import random

class Quoridor(object):


    #Constantes

    CELL_SIZE = 40  # Taille d'une cellule
    PADDING = 14  # Espace entre les cellules
    OUTER_PADDING = 10  # Espace autour de la grille pour la centrer

    #Couleurs
    BG="gray"
    BARRIER="orange"
    CASE="white"
    J1="purple"
    J2="cyan"

    def __init__(self,state):
        """
        Permet d'initialiser les variables et le plateau de jeu

        :param state: permet de préciser de quelle situation on veut partir
        :type state: State
        :return
        :rtype: None
        """

        #Jeu en cours
        self.jeu=True

        #Stocker l'état courant pour limiter les coûts d'actualisations
        self.current = state

        #Creer les elements graphiques
        self.root = tk.Tk()
        self.top_frame = tk.Frame(self.root, bg=Quoridor.BG)
        self.counter_label_top = tk.Label(self.top_frame, text=f"{state.p2_walls}", bg=Quoridor.BG, fg="black", font=("Arial", 20))
        self.rectangle_top = tk.Label(self.top_frame, width=10, bg=Quoridor.BARRIER)
        self.canvas_haut = tk.Canvas(self.top_frame, width=35, height=30, bg=Quoridor.BG, highlightthickness=0)
        self.rond_haut = self.canvas_haut.create_oval(15, 10, 30, 25, fill=("green" if not state.player1 else Quoridor.BG), outline=Quoridor.BG)
        self.frame = tk.Frame(self.root, padx=Quoridor.OUTER_PADDING, pady=Quoridor.OUTER_PADDING, bg=Quoridor.BG)
        self.canvas = tk.Canvas(self.frame, width=9 * (Quoridor.CELL_SIZE + Quoridor.PADDING), height=9 * (Quoridor.CELL_SIZE + Quoridor.PADDING), bg=Quoridor.BG,
                           highlightthickness=0)
        self.input_joueur = tk.Frame(self.frame, padx=Quoridor.OUTER_PADDING, pady=Quoridor.OUTER_PADDING, bg=Quoridor.BG)
        self.v1 = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self.input_joueur, text='Horizontal?', variable=self.v1, onvalue=1, offvalue=0, bg=Quoridor.BG)
        self.v = tk.StringVar()
        self.entry = tk.Entry(self.input_joueur, textvariable=self.v, width=10)

        # Boucle pour créer une grille de 9x9 avec des labels espacés
        self.cells = {}
        for y in range(9):
            for x in range(9):
                x1 = x * (Quoridor.CELL_SIZE + Quoridor.PADDING)
                y1 = y * (Quoridor.CELL_SIZE + Quoridor.PADDING)
                x2 = x1 + Quoridor.CELL_SIZE
                y2 = y1 + Quoridor.CELL_SIZE
                cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill=(Quoridor.J1 if (state.p1_pos==(x,y)) else Quoridor.J2 if (state.p2_pos==(x,y)) else Quoridor.CASE), outline="black")
                self.cells[(x, y)] = cell

                # Chargement des barrières horizontales
                if (state.h_walls >> (y * 8 + x)) & 1:  # On décale vers la position qui nous intéresse puis on regarde si le bit de poids faible vaut 1
                    x1 = x * (self.CELL_SIZE + self.PADDING)
                    x2 = x1 + 2 * self.CELL_SIZE + self.PADDING
                    y1 = y * (self.CELL_SIZE + self.PADDING) + self.CELL_SIZE + self.PADDING / 2
                    self.canvas.create_line(x1, y1, x2, y1, fill=self.BARRIER, width=8, tags="barrier")

                # Chargement des barrières verticales
                if (state.v_walls >> (y * 8 + x)) & 1:  # On décale vers la position qui nous intéresse puis on regarde si le bit de poids faible vaut 1
                    x1 = x * (self.CELL_SIZE + self.PADDING) + self.CELL_SIZE + self.PADDING / 2
                    y1 = y * (self.CELL_SIZE + self.PADDING)
                    y2 = y1 + 2 * self.CELL_SIZE + self.PADDING
                    self.canvas.create_line(x1, y1, x1, y2, fill=self.BARRIER, width=8, tags="barrier")

        self.bottom_frame = tk.Frame(self.root, bg=Quoridor.BG)
        self.counter_label_bottom = tk.Label(self.bottom_frame, text=f"{state.p1_walls}", bg=Quoridor.BG, fg="black", font=("Arial", 20))
        self.rectangle_bottom = tk.Label(self.bottom_frame, width=10, bg=Quoridor.BARRIER)
        self.canvas_bas = tk.Canvas(self.bottom_frame, width=35, height=30, bg=Quoridor.BG, highlightthickness=0)
        self.rond_bas = self.canvas_bas.create_oval(15, 10, 30, 25, fill=("green" if state.player1 else Quoridor.BG), outline=Quoridor.BG)

        #On place et parametre les elements graphiques
        #self.init_grid()

        self.root.title("Quoridor")
        self.root.geometry("600x625+300+10")
        self.root.configure(bg=Quoridor.BG)  # Fond pour la fenêtre principale
        self.top_frame.pack(anchor="w", pady=(Quoridor.OUTER_PADDING, 10), padx=Quoridor.OUTER_PADDING)
        self.counter_label_top.pack(side="left")

        # Rectangle orange en haut
        self.rectangle_top.pack(side="left", padx=(10, 0))
        self.rectangle_top.config(height=1, pady=1)

        self.canvas_haut.pack()
        self.frame.pack()
        self.canvas.grid(row=0, column=0)
        self.input_joueur.grid(row=0, column=1)
        self.checkbox.grid(row=0, column=0)
        self.entry.grid(row=1, column=0)

        # Lier les events
        self.entry.bind("<Return>", self.traiter)
        self.canvas.bind("<Button-1>", self.callback)

        self.bottom_frame.pack(anchor="w", pady=(10, Quoridor.OUTER_PADDING), padx=Quoridor.OUTER_PADDING)
        self.counter_label_bottom.pack(side="left")
        self.rectangle_bottom.pack(side="left", padx=(10, 0))
        self.rectangle_bottom.config(height=1, pady=1)
        self.canvas_bas.pack()

    #Redefinition de la fonction print
    def __str__(self):
        self.root.mainloop()
        return ""

    # Fonction qui permet de lire un état et de mettre à jour la fenêtre graphique en conséquent
    def setState(self, state):
        """
        Permet de charger une nouvelle configuration de partie

        :param state: permet de préciser de quelle situation on veut partir
        :type state: State
        :return
        :rtype: None
        """

        self.current = state


        #Chargement des compteurs de barrières
        self.counter_label_top.config(text=f"{state.p2_walls}")
        self.counter_label_bottom.config(text=f"{state.p1_walls}")

        #Chargement du point de joueur actif
        self.canvas_bas.itemconfig(self.rond_bas, fill=Quoridor.BG)
        self.canvas_haut.itemconfig(self.rond_haut, fill=Quoridor.BG)
        if state.player1:
            self.canvas_bas.itemconfig(self.rond_bas, fill="green")
        else:
            self.canvas_haut.itemconfig(self.rond_haut, fill="green")

        #Suppression des anciennes barrières
        self.canvas.delete("barrier")

        for y in range(9):
            for x in range(9):
                # Chargement des barrières horizontales
                if (state.h_walls>>(y*8 +x)) & 1 and x<8 and y<8: #On décale vers la position qui nous intéresse puis on regarde si le bit de poids faible vaut 1
                    x1 = x * (self.CELL_SIZE + self.PADDING)
                    x2 = x1 + 2 * self.CELL_SIZE + self.PADDING
                    y1 = y * (self.CELL_SIZE + self.PADDING) + self.CELL_SIZE + self.PADDING / 2
                    self.canvas.create_line(x1, y1, x2, y1, fill=self.BARRIER, width=8, tags="barrier")

                # Chargement des barrières verticales
                if (state.v_walls >> (y * 8 + x)) & 1 and x<8 and y<8:#On décale vers la position qui nous intéresse puis on regarde si le bit de poids faible vaut 1
                    x1 = x * (self.CELL_SIZE + self.PADDING) + self.CELL_SIZE + self.PADDING / 2
                    y1 = y * (self.CELL_SIZE + self.PADDING)
                    y2 = y1 + 2 * self.CELL_SIZE + self.PADDING
                    self.canvas.create_line(x1, y1, x1, y2, fill=self.BARRIER, width=8, tags="barrier")

                #Chargement des positions de joueurs
                if state.p1_pos==(x,y):
                    self.canvas.itemconfig(self.cells[(x,y)], fill=Quoridor.J1)
                elif state.p2_pos==(x,y):
                    self.canvas.itemconfig(self.cells[(x,y)], fill=Quoridor.J2)
                else:
                    self.canvas.itemconfig(self.cells[(x,y)], fill=Quoridor.CASE)

    #Fonction qui permet de formater l'action
    def traiter(self,x):
        action=self.entry.get().replace(" ","")
        if self.current.action_valide(action):
                self.updateState(action)

    # Fonction qui traite le click et affiche la commande voulue dans l'entry
    def callback(self, event):
        """
        Permet de faciliter le jeu à l'utilisateur, écrit les coordonées dans l'entry suivant la position du click


        :param event: Evenement géré par un écouteur d'évènement de click
        """
        if self.v1.get():
            aux = str(event.x // 54) + " " + str(event.y // 54) + " 1"
        else:
            aux = str(event.x // 54) + " " + str(event.y // 54) + " 0"
        self.v.set(aux)
        self.traiter(0)
        #print(self.current.actions_possibles())

    # Fonction qui permet de mettre à jour la fenêtre graphique en fonction d'une action
    def updateState(self, action): #action={"z","q","s","d","xyh",...} avec x,y position du mur et h 0 ou 1 en fonction de son horizontalité
        """
        Permet d'effectuer une nouvelle action depuis l'état précedant

        :param action: permet de préciser quelle action on effectue
        :type action: str
        :return
        :rtype: None
        """

        moves = {
            'z': (0, -1),  # haut
            'q': (-1, 0),  # gauche
            's': (0, 1),  # bas
            'd': (1, 0)  # droite
        }
        if action in moves:
            # Déterminer le joueur actif et sa position
            if self.current.player1:
                old_pos = self.current.p1_pos
                color = Quoridor.J1
            else:
                old_pos = self.current.p2_pos
                color = Quoridor.J2

            # Calculer la nouvelle position
            dx, dy = moves[action[0]]
            new_pos = (old_pos[0] + dx, old_pos[1] + dy)

            # Mettre à jour l'affichage et la position
            self.canvas.itemconfig(self.cells[old_pos], fill=Quoridor.CASE)
            if self.current.player1:
                self.current.p1_pos = new_pos

            else:
                self.current.p2_pos = new_pos
            self.canvas.itemconfig(self.cells[new_pos], fill=color)
            if self.current.player1 and self.current.p1_pos[1]==0:
                self.affichage_fin()
            elif (not self.current.player1) and self.current.p2_pos[0]==8:
                self.affichage_fin()


        else:
            if action[2]=="0":#Barrière verticale
                x,y=int(action[0]),int(action[1])

                x1 = x * (self.CELL_SIZE + self.PADDING) + self.CELL_SIZE + self.PADDING / 2
                y1 = y * (self.CELL_SIZE + self.PADDING)
                y2 = y1 + 2 * self.CELL_SIZE + self.PADDING
                self.canvas.create_line(x1, y1, x1, y2, fill=self.BARRIER, width=8)
                self.current.v_walls=self.current.v_walls | (1 << (y*8 +x))

            else:#Barrière horizontale
                x,y=int(action[0]),int(action[1])

                x1 = x * (self.CELL_SIZE + self.PADDING)
                x2 = x1 + 2 * self.CELL_SIZE + self.PADDING
                y1 = y * (self.CELL_SIZE + self.PADDING) + self.CELL_SIZE + self.PADDING / 2
                self.canvas.create_line(x1, y1, x2, y1, fill=self.BARRIER, width=8)
                self.current.h_walls = self.current.h_walls | (1 << (y * 8 + x))

            #Actualisation du compteur de barrières
            if self.current.player1:
                self.current.p1_walls -= 1
                self.counter_label_bottom.config(text=f"{self.current.p1_walls}")
            else:
                self.current.p2_walls -= 1
                self.counter_label_top.config(text=f"{self.current.p2_walls}")

        # Chargement du point de joueur actif
        self.current.player1 = not self.current.player1
        self.canvas_bas.itemconfig(self.rond_bas, fill=Quoridor.BG)
        self.canvas_haut.itemconfig(self.rond_haut, fill=Quoridor.BG)
        if self.current.player1:
            self.canvas_bas.itemconfig(self.rond_bas, fill="green")
        else:
            self.canvas_haut.itemconfig(self.rond_haut, fill="green")

    # Fonction d'indiquation de fin de partie (graphique)
    def affichage_fin(self):
        """
        Permet d'afficher une popup de fin de partie


        """
        self.jeu=False
        self.popup = tk.Toplevel(self.root)
        if self.current.p1_pos[1] == 0:
            self.popup.title("Joueur du bas à gagné la partie")
        else:
            self.popup.title("Joueur du haut à gagné la partie")

        image = tk.PhotoImage(file="photos/" + str(random.randint(0, 8)) + ".png")
        label = tk.Label(self.popup, image=image)
        label.image = image
        label.pack()
        self.fermer()
        """
        if self.vrai_joueurs:
            time.sleep(4)
            self.root.destroy()"""

    # Fonction qui demande au mainloop de fermer le plateau de jeu
    def fermer(self):
        """
        Demande au mainloop de fermer le plateau de jeu proprement


        """
        self.root.after(4000, self.close)

    # Permet de fermer le mainloop de manière sécurisée
    def close(self):
        """
        Fonction éxécutée par la mainloop pour fermer la fenetre graphique du jeu


        """

        for widget in self.root.winfo_children():
            widget.destroy()
        self.entry.destroy()

        self.popup.destroy()
        self.root.destroy()