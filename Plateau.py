import tkinter as tk
import random
import threading
import time

class Quoridor(object):

    #Constantes

    # Dimensions de la grille
    ROWS, COLS = 9, 9
    CELL_SIZE = 40  # Taille d'une cellule
    PADDING = 14  # Espace entre les cellules
    OUTER_PADDING = 10  # Espace autour de la grille pour la centrer

    #Couleurs
    BG="gray"
    BARRIER="orange"
    CASE="white"
    J1="purple"
    J2="cyan"

    def __init__(self,nb=10):
        #Au tour du premier joueur
        self.premier_joueur = True

        #Jeu en cours
        self.jeu=True

        # Nb de barrières par joueurs
        #self.nb1 = nb
        #self.nb2 = nb

        self.etat=[4,8,4,0,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#x1,y1,x2,y2,nb1,nb2,liste des positions;0:rien,1:horizontale,2:verticale

        # Localisations des joueurs
        #self.etat[1 ,self.etat[0= (8, 4)  # y,x
        #self.etat[3,self.etat[2 = (0, 4)  # y,x

        # Ensemble des murs placés dans le jeu
        #self.murs = set()

        # Dictionnaire des voisins accessibles depuis chaque case
        self.plateau = {}
        for x in range(9):
            for y in range(9):
                ens_aux = set()

                if x != 0:
                    ens_aux.add((x - 1, y))
                if x != 8:
                    ens_aux.add((x + 1, y))
                if y != 0:
                    ens_aux.add((x, y - 1))
                if y != 8:
                    ens_aux.add((x, y + 1))

                self.plateau[(x, y)] = ens_aux

        #Creer les elements graphiques
        self.root = tk.Tk()
        self.top_frame = tk.Frame(self.root, bg=Quoridor.BG)
        self.counter_label_top = tk.Label(self.top_frame, text="10", bg=Quoridor.BG, fg="black", font=("Arial", 20))
        self.rectangle_top = tk.Label(self.top_frame, width=10, bg=Quoridor.BARRIER)
        self.canvas_haut = tk.Canvas(self.top_frame, width=35, height=30, bg=Quoridor.BG, highlightthickness=0)
        self.rond_haut = self.canvas_haut.create_oval(15, 10, 30, 25, fill=Quoridor.BG, outline=Quoridor.BG)
        self.frame = tk.Frame(self.root, padx=Quoridor.OUTER_PADDING, pady=Quoridor.OUTER_PADDING, bg=Quoridor.BG)
        self.canvas = tk.Canvas(self.frame, width=Quoridor.COLS * (Quoridor.CELL_SIZE + Quoridor.PADDING), height=Quoridor.ROWS * (Quoridor.CELL_SIZE + Quoridor.PADDING), bg=Quoridor.BG,
                           highlightthickness=0)
        self.input_joueur = tk.Frame(self.frame, padx=Quoridor.OUTER_PADDING, pady=Quoridor.OUTER_PADDING, bg=Quoridor.BG)
        self.v1 = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self.input_joueur, text='Horizontal?', variable=self.v1, onvalue=1, offvalue=0, bg=Quoridor.BG)
        self.v = tk.StringVar()
        self.entry = tk.Entry(self.input_joueur, textvariable=self.v, width=10)

        # Boucle pour créer une grille de 9x9 avec des labels espacés
        self.cells = {}
        for i in range(Quoridor.ROWS):
            for j in range(Quoridor.COLS):
                x1 = j * (Quoridor.CELL_SIZE + Quoridor.PADDING)
                y1 = i * (Quoridor.CELL_SIZE + Quoridor.PADDING)
                x2 = x1 + Quoridor.CELL_SIZE
                y2 = y1 + Quoridor.CELL_SIZE
                cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill=Quoridor.CASE, outline="black")
                self.cells[(i, j)] = cell
        self.bottom_frame = tk.Frame(self.root, bg=Quoridor.BG)
        self.counter_label_bottom = tk.Label(self.bottom_frame, text="10", bg=Quoridor.BG, fg="black", font=("Arial", 20))
        self.rectangle_bottom = tk.Label(self.bottom_frame, width=10, bg=Quoridor.BARRIER)
        self.canvas_bas = tk.Canvas(self.bottom_frame, width=35, height=30, bg=Quoridor.BG, highlightthickness=0)
        self.rond_bas = self.canvas_bas.create_oval(15, 10, 30, 25, fill="green", outline=Quoridor.BG)

        #On place et parametre les elements graphiques
        self.init_grid()


    # Fonction pour mettre à jour le compteur de p1 ou pas (p2)
    def update_counter(self,p1):
        if p1:
            self.etat[4] = self.etat[4]-1
            self.counter_label_bottom.config(text=f"{self.etat[4]}")
            print("ok1")
        else:
            self.etat[5] = self.etat[5]-1
            self.counter_label_top.config(text=f"{self.etat[5]}")
            print("ok2")

    # Fonction pour afficher les bonhommes rouge et noir en fct de leur position avec b pour dire si on colorie ou si on efface
    def pions(self,b: bool):
        if b:
            self.canvas.itemconfig(self.cells[self.etat[1],self.etat[0]], fill=Quoridor.J1)
            self.canvas.itemconfig(self.cells[self.etat[3],self.etat[2]], fill=Quoridor.J2)
        else:
            self.canvas.itemconfig(self.cells[self.etat[1],self.etat[0]], fill=Quoridor.CASE)
            self.canvas.itemconfig(self.cells[self.etat[3],self.etat[2]], fill=Quoridor.CASE)

    # Fonction pour deplacer un bonhomme selon un string: H->haut B->bas ... le reste-> rien
    def deplacer(self,string: str):
        #print("appel")
        match string:
            case "Z":

                if self.premier_joueur and self.etat[1] >= 1 and (self.etat[0], self.etat[1] - 1) in self.plateau[(self.etat[0], self.etat[1])]:
                    self.pions(False)
                    self.etat[1],self.etat[0] = (self.etat[1] - 1, self.etat[0])
                    self.pions(True)
                    if self.etat[1] == 0:
                        self.jeu = False
                    self.tour_suivant(False)
                elif (not self.premier_joueur) and self.etat[3] >= 1 and (self.etat[2], self.etat[3] - 1) in self.plateau[(self.etat[2], self.etat[3])]:
                    self.pions(False)
                    self.etat[3],self.etat[2] = (self.etat[3] - 1, self.etat[2])
                    self.pions(True)
                    self.tour_suivant(False)
            case "Q":
                if self.premier_joueur and self.etat[0] >= 1 and (self.etat[0] - 1, self.etat[1]) in self.plateau[(self.etat[0], self.etat[1])]:
                    self.pions(False)
                    self.etat[1],self.etat[0] = (self.etat[1], self.etat[0] - 1)
                    self.pions(True)
                    self.tour_suivant(False)
                elif (not self.premier_joueur) and self.etat[2] >= 1 and (self.etat[2] - 1, self.etat[3]) in self.plateau[(self.etat[2], self.etat[3])]:

                    self.pions(False)
                    self.etat[3],self.etat[2] = (self.etat[3], self.etat[2] - 1)
                    self.pions(True)
                    self.tour_suivant(False)
            case "D":
                if self.premier_joueur and self.etat[0] <= 7 and (self.etat[0] + 1, self.etat[1]) in self.plateau[(self.etat[0], self.etat[1])]:
                    self.pions(False)
                    self.etat[1],self.etat[0] = (self.etat[1], self.etat[0] + 1)
                    self.pions(True)
                    self.tour_suivant(False)
                elif (not (self.premier_joueur)) and self.etat[2] <= 7 and (self.etat[2] + 1, self.etat[3]) in self.plateau[(self.etat[2], self.etat[3])]:
                    self.pions(False)
                    self.etat[3],self.etat[2] = (self.etat[3], self.etat[2] + 1)
                    self.pions(True)
                    self.tour_suivant(False)
            case "S":
                if self.premier_joueur and self.etat[1] <= 7 and (self.etat[0], self.etat[1] + 1) in self.plateau[(self.etat[0], self.etat[1])]:
                    self.pions(False)
                    self.etat[1],self.etat[0] = (self.etat[1] + 1, self.etat[0])
                    self.pions(True)
                    self.tour_suivant(False)
                elif (not (self.premier_joueur)) and self.etat[3] <= 7 and (self.etat[2], self.etat[3] + 1) in self.plateau[(self.etat[2], self.etat[3])]:
                    self.pions(False)
                    self.etat[3],self.etat[2] = (self.etat[3] + 1, self.etat[2])
                    self.pions(True)
                    if self.etat[3] == 8:
                        self.jeu = False
                    self.tour_suivant(False)

            case a:
                print(f"Erreur9980: string |{a}| interdit")

    # Fonction pour passer au tour suivant avec b qui indique si on doit decompter ou pas le compteur de barrieres
    def tour_suivant(self,b: bool):
        self.premier_joueur = not self.premier_joueur
        if b:
            self.update_counter(not self.premier_joueur)
        if self.premier_joueur:
            self.canvas_bas.itemconfig(self.rond_bas, fill="green")
            self.canvas_haut.itemconfig(self.rond_haut, fill=Quoridor.BG)
        else:
            self.canvas_bas.itemconfig(self.rond_bas, fill=Quoridor.BG)
            self.canvas_haut.itemconfig(self.rond_haut, fill="green")

        self.entry.delete(0, tk.END)

    # Fonction qui joue le tour d'une personne suivant l'entry
    def action(self,event=None,act=None):
        if self.jeu:
            try:
                if act is None:
                    tab = [int(i) for i in self.entry.get().split()]
                else:
                    tab = [act[0],act[1],act[2]]
                aux = 0
                #print(self.premier_joueur,"|pr_j")
                if self.premier_joueur:
                    aux = self.etat[4]
                else:
                    aux = self.etat[5]
                if (aux > 0) and (len(tab) == 3) and ((tab[2] == 1) or (tab[2] == 0)) and (tab[0] >= 0) and (tab[0] <= 7) and (tab[1] >= 0) and (tab[1] <= 7):
                    self.add_line(tab[0], tab[1], bool(tab[2]))

                    if self.jeu:
                        reward = 0
                    else:
                        reward = 1
                    #print(self.etat, reward)
                    return (self.etat, reward)
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
                    return (self.etat,reward)
                except Exception as e:
                    print("Erreur5048")
                    print(e)

            if not self.jeu:
                self.affichage_fin()


    #Fonction qui traite le click et affiche la commande voulue dans l'entry
    def callback(self,event):
        if self.v1.get():
            aux = str(event.x // 54) + " " + str(event.y // 54) + " 1"
        else:
            aux = str(event.x // 54) + " " + str(event.y // 54) + " 0"
        self.v.set(aux)

    # Fonction pour verifier qu'il existe au moins un chemin solution pour chaque joueur
    def existe_sol(self,case, ord, visites) -> bool:
        if visites is None:
            visites = set()
        if case[1] == ord:
            return True
        visites.add(case)
        for voisin in self.plateau.get(case):
            if voisin not in visites:
                if self.existe_sol(voisin, ord, visites):
                    return True

        return False

    # Fonction pour ajouter un trait orange horizontal ou vertical entre deux cellules
    # On lui donne x,y coordonees de la cellule en haut a gauche et h=True si horizontal
    def add_line(self,x: int, y: int, h=True,reset=False):
        if reset:
            if h:
                # Calculer les coordonnées du trait en fonction des indices des cellules
                x1 = x * (Quoridor.CELL_SIZE + Quoridor.PADDING)
                x2 = x1 + 2 * Quoridor.CELL_SIZE + Quoridor.PADDING
                y1 = y * (Quoridor.CELL_SIZE + Quoridor.PADDING) + Quoridor.CELL_SIZE + Quoridor.PADDING / 2

                # Dessiner le trait orange
                self.canvas.create_line(x1, y1, x2, y1, fill=Quoridor.BG, width=8)
            else:
                # Calculer les coordonnées du trait en fonction des indices des cellules
                x1 = x * (Quoridor.CELL_SIZE + Quoridor.PADDING) + Quoridor.CELL_SIZE + Quoridor.PADDING / 2
                y1 = y * (Quoridor.CELL_SIZE + Quoridor.PADDING)
                y2 = y1 + 2 * Quoridor.CELL_SIZE + Quoridor.PADDING
                # Dessiner le trait orange
                self.canvas.create_line(x1, y1, x1, y2, fill=Quoridor.BG, width=8)
        else:
            if not (0 <= x <= 7 and 0 <= y <= 7):
                print(f"L'emplacement x: {x}, y: {y} est interdit")
            else:
                if h:
                    #if ((x, y, int(h)) not in self.murs) and ((x - 1, y, int(h)) not in self.murs) and ((x + 1, y, int(h)) not in self.murs) and ((x, y, 1 - int(h)) not in self.murs):
                    if (y== 8 or x==8 or self.etat[y * 8+x+6] == 0) and (x==0 or self.etat[y * 8+x+5] != 1) and (x==7 or self.etat[y * 8+x+7] != 1):
                        self.plateau[(x, y)].remove((x, y + 1))
                        self.plateau[(x, y + 1)].remove((x, y))
                        self.plateau[(x + 1, y)].remove((x + 1, y + 1))
                        self.plateau[(x + 1, y + 1)].remove((x + 1, y))
                        if self.existe_sol((self.etat[2], self.etat[3]), 8, None) and self.existe_sol((self.etat[0], self.etat[1]), 0, None):
                            # Calculer les coordonnées du trait en fonction des indices des cellules
                            x1 = x * (Quoridor.CELL_SIZE + Quoridor.PADDING)
                            x2 = x1 + 2 * Quoridor.CELL_SIZE + Quoridor.PADDING
                            y1 = y * (Quoridor.CELL_SIZE + Quoridor.PADDING) + Quoridor.CELL_SIZE + Quoridor.PADDING / 2

                            # Dessiner le trait orange
                            self.canvas.create_line(x1, y1, x2, y1, fill=Quoridor.BARRIER, width=8)

                            #self.murs.add((x, y, int(h)))
                            self.etat[y * 8+x+6]=1

                            self.tour_suivant(True)
                        else:
                            self.plateau[(x, y)].add((x, y + 1))
                            self.plateau[(x, y + 1)].add((x, y))
                            self.plateau[(x + 1, y)].add((x + 1, y + 1))
                            self.plateau[(x + 1, y + 1)].add((x + 1, y))
                            print(f"L'emplacement x: {x}, y: {y} bloque un des joueurs")
                    else:
                        print(f"L'emplacement x: {x}, y: {y} est occupé par un autre mur")
                else:
                    #if ((x, y, int(h)) not in self.murs) and ((x, y - 1, int(h)) not in self.murs) and ((x, y + 1, int(h)) not in self.murs) and ((x, y, 1 - int(h)) not in self.murs):
                    if (y== 8 or x==8 or self.etat[y * 8 + x + 6] == 0) and (y == 0 or self.etat[(y-1) * 8 + x + 6] != 2) and (y == 7 or self.etat[(y+1) * 8 + x + 7] != 2):
                        self.plateau[(x, y)].remove((x + 1, y))
                        self.plateau[(x + 1, y)].remove((x, y))
                        self.plateau[(x + 1, y + 1)].remove((x, y + 1))
                        self.plateau[(x, y + 1)].remove((x + 1, y + 1))
                        if self.existe_sol((self.etat[2], self.etat[3]), 8, None) and self.existe_sol((self.etat[0], self.etat[1]), 0, None):
                            # Calculer les coordonnées du trait en fonction des indices des cellules
                            x1 = x * (Quoridor.CELL_SIZE + Quoridor.PADDING) + Quoridor.CELL_SIZE + Quoridor.PADDING / 2
                            y1 = y * (Quoridor.CELL_SIZE + Quoridor.PADDING)
                            y2 = y1 + 2 * Quoridor.CELL_SIZE + Quoridor.PADDING
                            # Dessiner le trait orange
                            self.canvas.create_line(x1, y1, x1, y2, fill=Quoridor.BARRIER, width=8)

                            #self.murs.add((x, y, int(h)))
                            self.etat[y * 8 + x + 6] = 2
                            self.tour_suivant(True)
                        else:
                            self.plateau[(x, y)].add((x + 1, y))
                            self.plateau[(x + 1, y)].add((x, y))
                            self.plateau[(x + 1, y + 1)].add((x, y + 1))
                            self.plateau[(x, y + 1)].add((x + 1, y + 1))
                            print(f"L'emplacement x: {x}, y: {y} bloque un des joueurs")
                    else:
                        print(f"L'emplacement x: {x}, y: {y} est occupé par un autre mur")

    #Fonction d'indiquation de fin de partie (graphique)
    def affichage_fin(self):
        popup = tk.Toplevel(self.root)
        if self.etat[1]==0:
            popup.title("ROUGE à gagné la partie")
        else:
            popup.title("NOIR à gagné la partie")

        image = tk.PhotoImage(file="photos/"+str(random.randint(0,8))+".png")
        label = tk.Label(popup, image=image)
        label.image = image
        label.pack()

    #Fonction pour construire et ordonner le Quoridor
    def init_grid(self):

        self.root.title("Quoridor")
        self.root.geometry("600x625+300+10")
        self.root.configure(bg=Quoridor.BG)  # Fond gris pour la fenêtre principale
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

        # On affiche les pions de depart
        self.pions(True)

        # Démarrer la boucle principale
        self.root.mainloop()

    #Fonction qui applique une action au jeu et renvoie l'etat et la reward
    def tour(self,etat):
        pass

class Joueur(object):

    ALPHA=1 #Importance de la position de l'adversaire par rapport à la notre
    PROBA_DEPL=60#probabilité de se déplacer lorsque on joue "aléatoirement"

    # Player
    def __init__(self, humain:bool,J1:bool,V_J1,V_J2):
        if J1:
            self.V_self = V_J1 #On regarde si ca existe et sinon on le cree ==> (x1,y1,x2,y2,nb,murs)
            self.V_opponent = V_J2
        else:
            self.V_opponent = V_J1
            self.V_self = V_J2

        self.J1=J1
        self.humain = humain
        self.historique = []
        self.win_nb = 0.
        self.lose_nb = 0.
        self.rewards = []
        self.eps = 0.99

    def reset_stat(self):

        self.win_nb = 0
        self.lose_nb = 0
        self.rewards = []

    # Fonction pour verifier qu'il existe au moins un chemin solution pour chaque joueur
    def existe_sol(self,case, ord, visites,etat) -> bool:
        if visites is None:
            visites = set()
        if case[1] == ord:
            return True
        visites.add(case)
        x,y=case[0],case[1]
        dispos=[]
        #if y!=0 and ((x,y-1,1) not in murs) and ((x-1,y-1,1) not in murs):
        if y != 0 and (x==8 or etat[(y-1) * 8 + x + 6] != 1) and (x==0 or etat[(y-1) * 8 + x + 5] != 1):
            dispos.append((x,y-1))

        #if x!=0 and ((x-1,y,0) not in murs) and ((x-1,y-1,0) not in murs):
        if x != 0 and (y== 8 or etat[y * 8 + x + 5] != 2) and (y == 0 or etat[(y - 1) * 8 + x + 5] != 2):
            dispos.append((x-1,y))

        #if y!=8 and ((x,y,1) not in murs) and ((x-1,y,1) not in murs):
        if y != 8 and (x==8 or etat[y * 8 + x + 6] != 1) and (x == 0 or etat[y * 8 + x + 5] != 1):
            dispos.append((x,y+1))

        #if x!=8 and ((x,y,0) not in murs) and ((x,y-1,0) not in murs):
        if x != 8 and (y== 8 or etat[y * 8 + x + 6] != 2) and (y == 0 or etat[(y - 1) * 8 + x + 6] != 2):
            dispos.append((x+1,y))

        for voisin in dispos:
            if voisin not in visites:
                if self.existe_sol(voisin, ord, visites,etat):
                    return True

        return False

    #Fonction qui renvoie l'etat dans lequel on arrive après l'action
    def appliquer_action(self,etat,action):
        res=etat[:]#On copie etat
        if action=="Z":
            if self.J1:
                res[1]-=1
            else:
                res[3]-=1
        elif action=="Q":
            if self.J1:
                res[0]-=1
            else:
                res[2]-=1

        elif action=="S":
            if self.J1:
                res[1]+=1
            else:
                res[3]+=1

        elif action=="D":
            if self.J1:
                res[0]+=1
            else:
                res[2]+=1

        else:
            if self.J1:
                if action[2]==0:
                    res[action[1]*8 + action[0] + 6]=2
                else:
                    res[action[1] * 8 + action[0] + 6] = 1
                res[4]-=1
            else:
                if action[2] == 0:
                    res[action[1] * 8 + action[0] + 6] = 2
                else:
                    res[action[1] * 8 + action[0] + 6] = 1
                res[5]-=1

        return res

    #Fonction qui calcule les actions possibles
    def actions_possibles(self,etat):
        x1, y1, x2, y2, nb1, nb2 = etat[0],etat[1],etat[2],etat[3],etat[4],etat[5]  # murs:set((x,y,h))
        actions = []
        if self.J1:
            x, y, nb = x1, y1, nb1
        else:
            x, y, nb = x2, y2, nb2
        cpt = 0
        # Ajout des actions possibles (cf ligne 418:432 ; fct existe_sol de classe Joueur)
        if y != 0 and (x==8 or etat[(y - 1) * 8 + x + 6] != 1) and (x == 0 or etat[(y - 1) * 8 + x + 5] != 1):
            actions.append("Z")
            cpt += 1

        if x != 0 and (y== 8 or etat[y * 8 + x + 5] != 2) and (y == 0 or etat[(y - 1) * 8 + x + 5] != 2):
            actions.append("Q")
            cpt += 1

        if y != 8 and (x==8 or etat[y * 8 + x + 6] != 1) and (x == 0 or etat[y * 8 + x + 5] != 1):
            actions.append("S")
            cpt += 1

        if x != 8 and (y== 8 or etat[y * 8 + x + 6] != 2) and (y == 0 or etat[(y - 1) * 8 + x + 6] != 2):
            actions.append("D")
            cpt += 1
        #print(nb,"aieaieaie")
        if nb > 0:
            for y in range(8):
                for x in range(8):
                    # essai d'ajout des horizontales
                    if ( etat[y * 8+x+6] == 0) and (x==0 or etat[y * 8+x+5] != 1) and (x==7 or etat[y * 8+x+7] != 1):
                        #murs.add((x, y, 1))
                        etat[y * 8+x+6]=1
                        if self.existe_sol((x1, y1), 0,None, etat) and self.existe_sol((x2, y2), 8,None, etat):
                            actions.append((x, y, 1))
                        #murs.remove((x, y, 1))
                        etat[y * 8 + x + 6] = 0

                    # essai d'ajout des verticales
                    if etat[y * 8 + x + 6] == 0 and (y == 0 or etat[(y - 1) * 8 + x + 6] != 2) and (y == 7 or etat[(y + 1) * 8 + x + 6] != 2):

                        #murs.add((x, y, 0))
                        etat[y * 8 + x + 6] = 2
                        if self.existe_sol((x1, y1), 0, None, etat) and self.existe_sol((x2, y2), 8,None, etat):
                            actions.append((x, y, 0))
                        #murs.remove((x, y, 0))
                        etat[y * 8 + x + 6] = 0
        return actions,cpt

    #Fonction d'exploitation
    def greedy_step(self, etat):

        vmax = None
        vi = None

        actions,_ = self.actions_possibles(etat)

        for i in range(len(actions)):
            a = actions[i]
            etat_suivant=tuple(self.appliquer_action(etat,a))
            if etat_suivant not in self.V_self:
                self.V_self[etat_suivant]=0.
            myself=self.V_self[etat_suivant]
            if etat_suivant not in self.V_opponent:
                self.V_opponent[etat_suivant] = 0.
            opponent=self.V_opponent[etat_suivant]

            if vmax is None or vmax < (myself - Joueur.ALPHA * opponent): # dans les alumettes on cherche a donner la pire situation a son adversaire car on a une situation commune or ici le plateau est commun mais pas la pos
                vmax = (myself - Joueur.ALPHA * opponent) #On cherche a prendre l'action qui maximise la difference des situations
                vi = i
        return actions[vi]


    def play(self, state):
        if not self.humain:
            # Take random action
            if random.uniform(0, 1) < self.eps:
                p = random.randint(0, 100)
                actions,cpt=self.actions_possibles(state)
                #print(actions)
                #print(cpt)
                if p<Joueur.PROBA_DEPL or cpt==len(actions):
                    return actions[random.randint(0, cpt-1)]
                else:
                    return actions[random.randint(cpt, len(actions)-1)]
            else:  # Or greedy action
                return self.greedy_step(state)
        else:
            action = int(input("$>"))
            return action

    def add_transition(self, n_tuple):
        self.historique.append(n_tuple)
        s, a, r, sp = n_tuple
        self.rewards.append(r)

    def train(self):
        if self.humain:
            return

        # Update the value function if this player is not human
        for transition in reversed(self.historique):
            s, a, r, sp = transition
            t = tuple(s)
            if r == 0:

                self.V_self[t] = self.V_self[t] + 0.001 * (self.V_self[tuple(sp)] - self.V_self[t])
            else:
                self.V_self[t] = self.V_self[t] + 0.001 * (r - self.V_self[t])

        self.historique = []


def play(jeu,j1, j2):



    joueurs = [j1, j2]
    state=[4,8,4,0,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    print(len(state))
    p = 0
    while jeu.jeu:
        #print(p%2 +1==jeu.J1)
        time.sleep(0.2)
        action = joueurs[p % 2].play(state)
        #print(action)
        #jeu.action(act=action)
        #print(action)
        n_state, reward = jeu.action(act=action)
        #print(n_state,reward)

        #  Game is over. Ass stat
        if (reward != 0):
            # Update stat of the current player
            joueurs[p % 2].lose_nb += 1. if reward == -1 else 0
            joueurs[p % 2].win_nb += 1. if reward == 1 else 0
            # Update stat of the other player
            joueurs[(p + 1) % 2].lose_nb += 1. if reward == 1 else 0
            joueurs[(p + 1) % 2].win_nb += 1. if reward == -1 else 0

        # Add the reversed reward and the new state to the other player
        if p != 0:
            s, a, r, sp = joueurs[(p + 1) % 2].historique[-1]
            joueurs[(p + 1) % 2].historique[-1] = (s, a, reward * -1, n_state)

        joueurs[p % 2].add_transition((state, action, reward, None))

        state = n_state
        p += 1

    j1.train()
    j2.train()



if __name__ == '__main__':
    #game = Quoridor(10)
    #game.start_game()
    NB=10#Nombre de barrières au départ

    V1={}
    V2={}
    j1 = Joueur(humain=False, J1=True,V_J1=V1,V_J2=V2)
    j2 = Joueur(humain=False, J1=False,V_J1=V1,V_J2=V2)



    # Train the agent
    for i in range(0, 10000):
        if i % 10 == 0:
            j1.eps = max(j1.eps * 0.996, 0.05)
            j2.eps = max(j2.eps * 0.996, 0.05)
        jeu = Quoridor(NB)

        thread = threading.Thread(target=play, args=(jeu,j1,j2))
        thread.start()
        jeu.start_game()
        #play( jeu,j1, j2)
        print(f"fin de la {i} eme partie")
    j1.reset_stat()
    """
    # Affichage de la value fonction
    for key in j1.V_self:
        print(key, j1.V_self[key])
    print("--------------------------")"""

    # Jeu contre nous
    #while True:
        #play(game, j1, None, train=False)

"""

class StickGame(object):

    def __init__(self, nb):
        # @nb Number of stick to play with
        super(StickGame, self).__init__()
        self.original_nb = nb
        self.nb = nb

    def is_finished(self):
        # Check if the game is over @return Boolean
        if self.nb <= 0:
            return True
        return False

    def reset(self):
        # Reset the state of the game
        self.nb = self.original_nb
        return self.nb

    def display(self):
        # Display the state of the game
        print ("| " * self.nb)

    def step(self, action):
        # @action either 1, 2 or 3. Take an action into the environement
        self.nb -= action
        if self.nb <= 0:
            return None, -1
        else:
            return self.nb, 0

class StickPlayer(object):
    
        #Stick Player

    def __init__(self, is_human, size, trainable=True):
        # @nb Number of stick to play with
        super(StickPlayer, self).__init__()
        self.is_human = is_human
        self.history = []
        self.V = {}
        for s in range(1, size+1):
            self.V[s] = 0.
        self.win_nb = 0.
        self.lose_nb = 0.
        self.rewards = []
        self.eps = 0.99
        self.trainable = trainable

    def reset_stat(self):
        # Reset stat
        self.win_nb = 0
        self.lose_nb = 0
        self.rewards = []

    def greedy_step(self, state):
        # Greedy step
        actions = [1, 2, 3]
        vmin = None
        vi = None
        for i in range(0, 3):
            a = actions[i]
            if state - a > 0 and (vmin is None or vmin > self.V[state - a]):
                vmin = self.V[state - a]
                vi = i
        return actions[vi if vi is not None else 1]

    def play(self, state):
        # PLay given the @state (int)
        if self.is_human is False:
            # Take random action
            if random.uniform(0, 1) < self.eps:
                action = randint(1, 3)
            else: # Or greedy action
                action = self.greedy_step(state)
        else:
            action = int(input("$>"))
        return action

    def add_transition(self, n_tuple):
        # Add one transition to the history: tuple (s, a , r, s')
        self.history.append(n_tuple)
        s, a, r, sp = n_tuple
        self.rewards.append(r)

    def train(self):
        if not self.trainable or self.is_human is True:
            return

        # Update the value function if this player is not human
        for transition in reversed(self.history):
            s, a, r, sp = transition
            if r == 0:
                self.V[s] = self.V[s] + 0.001*(self.V[sp] - self.V[s])
            else:
                self.V[s] = self.V[s] + 0.001*(r - self.V[s])

        self.history = []

def play(game, p1, p2, train=True):
    state = game.reset()
    players = [p1, p2]
    random.shuffle(players)
    p = 0
    while game.is_finished() is False:

        if players[p % 2].is_human:
            game.display()

        action = players[p % 2].play(state)
        n_state, reward = game.step(action)

        #  Game is over. Ass stat
        if (reward != 0):
            # Update stat of the current player
            players[p % 2].lose_nb += 1. if reward == -1 else 0
            players[p % 2].win_nb += 1. if reward == 1 else 0
            # Update stat of the other player
            players[(p + 1) % 2].lose_nb += 1. if reward == 1 else 0
            players[(p + 1) % 2].win_nb += 1. if reward == -1 else 0

        # Add the reversed reward and the new state to the other player
        if p != 0:
            s, a, r, sp = players[(p + 1) % 2].history[-1]
            players[(p + 1) % 2].history[-1] = (s, a, reward * -1, n_state)

        players[p % 2].add_transition((state, action, reward, None))

        state = n_state
        p += 1
    if train:
        p1.train()
        p2.train()

if __name__ == '__main__':
    game = StickGame(12)

    # PLayers to train
    p1 = StickPlayer(is_human=False, size=12, trainable=True)
    p2 = StickPlayer(is_human=False, size=12, trainable=True)
    # Human player and random player
    human = StickPlayer(is_human=True, size=12, trainable=False)
    random_player = StickPlayer(is_human=False, size=12, trainable=False)

    # Train the agent
    for i in range(0, 10000):
        if i % 10 == 0:
            p1.eps = max(p1.eps*0.996, 0.05)
            p2.eps = max(p2.eps*0.996, 0.05)
        play(game, p1, p2)
    p1.reset_stat()

    # Display the value function
    for key in p1.V:
        print(key, p1.V[key])
    print("--------------------------")

    # Play agains a random player
    for _ in range(0, 1000):
        play(game, p1, random_player, train=False)
    print("p1 win rate", p1.win_nb/(p1.win_nb + p1.lose_nb))
    print("p1 win mean", np.mean(p1.rewards))

    # Play agains us
    while True:
        play(game, p1, human, train=False)
    
    
"""