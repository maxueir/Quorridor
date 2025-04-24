import State
import tkinter as tk
import threading

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


        #print("thread ok")

        #self.setState(state)

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







    # Fonction pour mettre à jour le compteur de p1 ou pas (p2)
    def update_counter(self,p1):
        """
        Permet de décrementer le compteur de l'un des joueur en fonction du booleen p1

        :param p1: indique si on veut changer le compteur de p1, sinon on change celui de p2
        :type p1: bool
        :return:
        :rtype None
        """
        if p1:
            self.etat.p1_walls-=1
            if self.display:
                self.counter_label_bottom.config(text=f"{self.etat.p1_walls}")

        else:

            self.etat.p2_walls-=1
            if self.display:
                self.counter_label_top.config(text=f"{self.etat.p2_walls}")


    # Fonction pour afficher les pions rouge et noir en fct de leur position avec b pour dire si on colorie ou si on efface
    def pions(self,b: bool):
        """
        Permet de colorier les deux cases des deux joueurs, on l'appelle avant deplacer les coordonées des joueurs pour effacer
        leur case avant de deplacer leur coordonnées et de ré-afficher leurs pions


        :param b: Si b est vrai, on colorie, sinon on efface
        :type b: bool
        :return:
        :rtype None
        """
        if self.display:
            if b:
                self.canvas.itemconfig(self.cells[self.etat.p1_pos], fill=Quoridor.J1)
                self.canvas.itemconfig(self.cells[self.etat.p2_pos], fill=Quoridor.J2)
            else:
                self.canvas.itemconfig(self.cells[self.etat.p1_pos], fill=Quoridor.CASE)
                self.canvas.itemconfig(self.cells[self.etat.p2_pos], fill=Quoridor.CASE)

    # Fonction pour deplacer un bonhomme selon un string: Z->haut S->bas ... le reste-> rien
    def deplacer(self,string: str):
        """
        Permet de déplacer le pion du joueur actif selon un string qui indique la direction


        :param string: Indique la direction dans laquelle on déplacer le joueur; Z,Q,S,D
        :type string: str
        :return:
        :rtype None
        """
        match string:
            case "Z":

                if self.premier_joueur and self.etat.p1_pos[1] >= 1 and self.voisins[self.etat.p1_pos[0],self.etat.p1_pos[1],0]:
                    self.pions(False)
                    self.etat.p1_pos=(self.etat.p1_pos[0], self.etat.p1_pos[1]-1)
                    self.pions(True)
                    if self.etat.p1_pos[1] == 0:
                        self.jeu = False
                    self.tour_suivant(False)
                elif (not self.premier_joueur) and self.etat.p2_pos[1]>=1 and self.voisins[self.etat.p2_pos[0],self.etat.p2_pos[1],0]:
                    self.pions(False)
                    self.etat.p2_pos=(self.etat.p2_pos[0], self.etat.p2_pos[1]-1)
                    self.pions(True)
                    self.tour_suivant(False)
            case "Q":
                if self.premier_joueur and self.etat.p1_pos[0] >= 1 and self.voisins[self.etat.p1_pos[0],self.etat.p1_pos[1],3]:
                    self.pions(False)
                    self.etat.p1_pos = (self.etat.p1_pos[0]-1, self.etat.p1_pos[1])
                    self.pions(True)
                    self.tour_suivant(False)
                elif (not self.premier_joueur) and self.etat.p2_pos[0] >= 1 and self.voisins[self.etat.p2_pos[0],self.etat.p2_pos[1],3]:

                    self.pions(False)
                    self.etat.p2_pos = (self.etat.p2_pos[0] - 1, self.etat.p2_pos[1])
                    self.pions(True)
                    self.tour_suivant(False)
            case "D":
                if self.premier_joueur and self.etat.p1_pos[0] <= 7 and self.voisins[self.etat.p1_pos[0],self.etat.p1_pos[1],1]:
                    self.pions(False)
                    self.etat.p1_pos = (self.etat.p1_pos[0] + 1, self.etat.p1_pos[1])
                    self.pions(True)
                    self.tour_suivant(False)
                elif (not (self.premier_joueur)) and self.etat.p2_pos[0] <= 7 and self.voisins[self.etat.p2_pos[0],self.etat.p2_pos[1],1]:
                    self.pions(False)
                    self.etat.p2_pos = (self.etat.p2_pos[0] + 1, self.etat.p2_pos[1])
                    self.pions(True)
                    self.tour_suivant(False)
            case "S":
                if self.premier_joueur and self.etat.p1_pos[1] <= 7 and self.voisins[self.etat.p1_pos[0],self.etat.p1_pos[1],2]:
                    self.pions(False)
                    self.etat.p1_pos = (self.etat.p1_pos[0], self.etat.p1_pos[1]+1)
                    self.pions(True)
                    self.tour_suivant(False)
                elif (not (self.premier_joueur)) and self.etat.p2_pos[1] <= 7 and self.voisins[self.etat.p2_pos[0],self.etat.p2_pos[1],2]:
                    self.pions(False)
                    self.etat.p2_pos = (self.etat.p2_pos[0], self.etat.p2_pos[1]+1)
                    self.pions(True)
                    if self.etat.p2_pos[1] == 8:
                        self.jeu = False
                    self.tour_suivant(False)

            case a:
                print(f"Erreur9980: string |{a}| interdit")

    # Fonction pour passer au tour suivant avec b qui indique si on doit decompter ou pas le compteur de barrieres
    def tour_suivant(self,b: bool):
        """
        Permet de changer de tour, donne la main à l'autre joueur et décompte au besoin les barrières


        :param b: Indique si on doit ou non decompter le nombre de barrière du joueur qui vient de finir son tour
        :type b: bool
        :return:
        :rtype None
        """
        self.premier_joueur = not self.premier_joueur
        if b:
            self.update_counter(not self.premier_joueur)

        if self.display:
            if self.premier_joueur:
                self.canvas_bas.itemconfig(self.rond_bas, fill="green")
                self.canvas_haut.itemconfig(self.rond_haut, fill=Quoridor.BG)
            else:
                self.canvas_bas.itemconfig(self.rond_bas, fill=Quoridor.BG)
                self.canvas_haut.itemconfig(self.rond_haut, fill="green")

            self.entry.delete(0, tk.END)

    # Fonction qui joue le tour d'une personne suivant l'entry
    def action(self,act=None):
        """
        Permet de jouer le tour d'un joueur suivant la valeur entrée dans la zone de jeu ou suivant act donnée


        :param act: Indique la position et l'orientation de la barrière à poser ou la direction pour déplacer le joueur
        :return: Renvoie un couple avec l'etat du plateau(liste d'entiers) et une récompense associés à l'action
        """
        if self.jeu:
            try:
                if act is None:
                    tab = [int(i) for i in self.entry.get().split()]
                else:
                    tab = [act[0],act[1],act[2]]
                aux = 0
                if self.premier_joueur:
                    aux = self.etat.p1_walls
                else:
                    aux = self.etat.p2_walls
                if (aux > 0) and (len(tab) == 3) and ((tab[2] == 1) or (tab[2] == 0)) and (tab[0] >= 0) and (tab[0] <= 7) and (tab[1] >= 0) and (tab[1] <= 7):
                    self.add_line(tab[0], tab[1], bool(tab[2]))

                    if self.jeu:
                        reward = 0
                    else:
                        reward = 1
                    #print(self.etat, reward)
                    #return (self.etat, reward)
                else:
                    print("Erreuuuur")
                    #print(aux)
                    #print(tab)



            except:
                try:
                    if act is None:
                        self.deplacer((self.entry.get()).upper())
                    else:
                        self.deplacer(act)
                    if self.jeu:
                        reward=0
                    else:
                        reward=1
                    #print(self.etat, reward)
                    #return (self.etat,reward)
                except Exception as e:
                    print("Erreur5048")
                    print(e)

            if not self.jeu:
                self.affichage_fin()
            #print(reward)
            return (self.etat, reward)




    # Fonction pour verifier qu'il existe au moins un chemin solution pour chaque joueur
    def existe_sol(self,case, ord, visites) -> bool:
        """
        Permet de dire si l'emplacement demandé pour la barrière ne bloque pas un joueur dans la situation courante du jeu


        :param case: Indique la position depuis laquelle la recherche de solution est lancée (couple d'entiers)
        :param ord: Indique si on peut atteindre une case d'ordonée ord
        :type ord: int
        :param visites: Utile pour la recherche de solution par parcours en profondeur (ensemble de couples d'entiers)
        :return: Renvoie un booléen qui indique si, depuis la position "case", on peut arriver à l'ordonnée "ord"
        :rtype : bool
        """
        if visites is None:
            visites = set()
        if case[1] == ord:
            return True
        visites.add(case)
        for i in range(4):
            if self.voisins[case[0], case[1], i]:
                if i==0:
                    voisin=(case[0], case[1]-1)
                elif i==1:
                    voisin=(case[0]+1, case[1])
                elif i==2:
                    voisin=(case[0], case[1]+1)
                elif i==3:
                    voisin=(case[0]-1, case[1])

                if voisin not in visites:
                    if self.existe_sol(voisin, ord, visites):
                        return True

        return False

    # Fonction pour ajouter un trait orange horizontal ou vertical entre deux cellules
    # On lui donne x,y coordonees de la cellule en haut a gauche et h=True si horizontal
    def add_line(self, x: int, y: int, h=True):
        """
        Permet d'ajouter une barrière sur le plateau graphique

        :param x: Position x de la barrière (0-7)
        :param y: Position y de la barrière (0-7)
        :param h: True pour horizontal, False pour vertical
        """
        if not (0 <= x <= 7 and 0 <= y <= 7):
            print(f"L'emplacement x: {x}, y: {y} est interdit")
            return

        # Vérifier si le mur est valide
        if h:
            # Vérifier mur horizontal
            if (self.etat.h_walls & (1 << (y * 8 + x))) or \
                    (x > 0 and (self.etat.h_walls & (1 << (y * 8 + x - 1)))) or \
                    (x < 7 and (self.etat.h_walls & (1 << (y * 8 + x + 1)))):
                print(f"L'emplacement x: {x}, y: {y} est occupé par un mur horizontal")
                return
        else:
            # Vérifier mur vertical
            if (self.etat.v_walls & (1 << (y * 8 + x))) or \
                    (y > 0 and (self.etat.v_walls & (1 << ((y - 1) * 8 + x)))) or \
                    (y < 7 and (self.etat.v_walls & (1 << ((y + 1) * 8 + x)))):
                print(f"L'emplacement x: {x}, y: {y} est occupé par un mur vertical")
                return

        # Sauvegarder l'état actuel des murs pour rollback si besoin
        old_h_walls = self.etat.h_walls
        old_v_walls = self.etat.v_walls

        # Ajouter le mur temporairement
        if h:
            self.etat.h_walls |= (1 << (y * 8 + x))
        else:
            self.etat.v_walls |= (1 << (y * 8 + x))

        # Mettre à jour la matrice des voisins
        self._update_neighbors(x, y, h, add=False)

        # Vérifier si les joueurs ont toujours un chemin
        if self._has_valid_paths():
            # Mur valide - confirmer l'ajout
            if self.display:
                self._draw_wall(x, y, h)

            # Décrémenter le compteur de murs
            if self.premier_joueur:
                self.etat.p1_walls -= 1
            else:
                self.etat.p2_walls -= 1

            self.tour_suivant(True)
        else:
            # Rollback - le mur bloque un joueur
            self.etat.h_walls = old_h_walls
            self.etat.v_walls = old_v_walls
            self._update_neighbors(x, y, h, add=True)
            print(f"L'emplacement x: {x}, y: {y} bloque un des joueurs")

    def _update_neighbors(self, x, y, is_horizontal, add):
        """Met à jour la matrice des voisins après ajout/suppression d'un mur"""
        if is_horizontal:
            # Mur horizontal bloque les déplacements verticaux
            self.voisins[x, y, 2] = add  # Bas
            self.voisins[x, y + 1, 0] = add  # Haut
            self.voisins[x + 1, y, 2] = add  # Bas
            self.voisins[x + 1, y + 1, 0] = add  # Haut
        else:
            # Mur vertical bloque les déplacements horizontaux
            self.voisins[x, y, 1] = add  # Droite
            self.voisins[x + 1, y, 3] = add  # Gauche
            self.voisins[x, y + 1, 1] = add  # Droite
            self.voisins[x + 1, y + 1, 3] = add  # Gauche

    def _has_valid_paths(self):
        """Vérifie que les deux joueurs ont un chemin vers leur objectif"""
        return (self._path_exists(self.etat.p1_pos, 0) and
                self._path_exists(self.etat.p2_pos, 8))

    def _path_exists(self, start, target_y):
        """Vérifie si un chemin existe avec A*"""
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}

        while not open_set.empty():
            current = open_set.get()[1]

            if current[1] == target_y:
                return True

            for neighbor in self._get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + abs(neighbor[1] - target_y)
                    open_set.put((f_score, neighbor))

        return False

    def _get_neighbors(self, pos):
        """Retourne les voisins accessibles depuis une position"""
        x, y = pos
        neighbors = []

        # Haut (0)
        if y > 0 and self.voisins[x, y, 0]:
            neighbors.append((x, y - 1))
        # Droite (1)
        if x < 8 and self.voisins[x, y, 1]:
            neighbors.append((x + 1, y))
        # Bas (2)
        if y < 8 and self.voisins[x, y, 2]:
            neighbors.append((x, y + 1))
        # Gauche (3)
        if x > 0 and self.voisins[x, y, 3]:
            neighbors.append((x - 1, y))

        return neighbors

    def _draw_wall(self, x, y, is_horizontal):
        """Dessine le mur sur le canvas"""
        if is_horizontal:
            x1 = x * (self.CELL_SIZE + self.PADDING)
            x2 = x1 + 2 * self.CELL_SIZE + self.PADDING
            y1 = y * (self.CELL_SIZE + self.PADDING) + self.CELL_SIZE + self.PADDING / 2
            self.canvas.create_line(x1, y1, x2, y1, fill=self.BARRIER, width=8)
        else:
            x1 = x * (self.CELL_SIZE + self.PADDING) + self.CELL_SIZE + self.PADDING / 2
            y1 = y * (self.CELL_SIZE + self.PADDING)
            y2 = y1 + 2 * self.CELL_SIZE + self.PADDING
            self.canvas.create_line(x1, y1, x1, y2, fill=self.BARRIER, width=8)

    #Fonction d'indiquation de fin de partie (graphique)
    def affichage_fin(self):
        """
        Permet d'afficher une popup de fin de partie


        """
        if self.display:
            self.popup = tk.Toplevel(self.root)
            if self.etat.p1_pos[1]==0:
                self.popup.title("Joueur du bas à gagné la partie")
            else:
                self.popup.title("Joueur du haut à gagné la partie")

            image = tk.PhotoImage(file="photos/"+str(random.randint(0,8))+".png")
            label = tk.Label(self.popup, image=image)
            label.image = image
            label.pack()
        """
        if self.vrai_joueurs:
            time.sleep(4)
            self.root.destroy()"""

    #Fonction pour construire et ordonner le Quoridor
    def init_grid(self):
        """
        Permet d'initialiser la grille graphique du quoridor


        """
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
        self.entry.bind("<Return>", self.action)
        self.canvas.bind("<Button-1>", self.callback)

        self.bottom_frame.pack(anchor="w", pady=(10, Quoridor.OUTER_PADDING), padx=Quoridor.OUTER_PADDING)
        self.counter_label_bottom.pack(side="left")
        self.rectangle_bottom.pack(side="left", padx=(10, 0))
        self.rectangle_bottom.config(height=1, pady=1)
        self.canvas_bas.pack()

    #Fonction qui lance le jeu
    def start_game(self,j1=None,j2=None):
        """
        Permet de lancer la partie


        """
        if self.display:
            # On affiche les pions de depart
            self.pions(True)

            # Démarrer la boucle principale
            self.root.mainloop()

    #Fonction qui demande au mainloop de fermer le plateau de jeu
    def fermer(self):
        """
        Demande au mainloop de fermer le plateau de jeu proprement


        """
        if self.display:
            self.root.after(4000, self.close)

    #Permet de fermer le mainloop de manière sécurisée
    def close(self):
        """
        Fonction éxécutée par la mainloop pour fermer la fenetre graphique du jeu


        """

        for widget in self.root.winfo_children():
            widget.destroy()
        self.entry.destroy()

        self.popup.destroy()
        self.root.destroy()