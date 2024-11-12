import tkinter as tk
import random

def create_grid():
    # Tour de premier_joueur
    global premier_joueur
    premier_joueur = True

    global jeu
    jeu=True

    # Nb de barrières par joueurs
    global nb1, nb2
    nb1 = 10
    nb2 = 10

    # Localisations des joueurs
    global loc1, loc2
    loc1 = (8, 4)  # y,x
    loc2 = (0, 4)  # y,x
    #test
    # dictionnaire des voisins accessibles depuis chaque case
    global plateau
    plateau = {}
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

            plateau[(x, y)] = ens_aux

    # Ensemble des murs placés dans le jeu
    global murs
    murs = set()

    # Créer une fenêtre principale
    root = tk.Tk()
    root.title("Quoridor")
    root.geometry("600x625+300+10")
    root.configure(bg="gray")  # Fond gris pour la fenêtre principale

    # Dimensions de la grille
    rows, cols = 9, 9
    cell_size = 40  # Taille d'une cellule
    padding = 14  # Espace entre les cellules
    outer_padding = 10  # Espace autour de la grille pour la centrer

    # Fonction pour mettre à jour le compteur de p1 ou pas
    def update_counter(p1):
        global nb1
        global nb2
        if p1:
            nb1 -= 1
            counter_label_bottom.config(text=f"{nb1}")
            print("ok1")
        else:
            nb2 -= 1
            counter_label_top.config(text=f"{nb2}")
            print("ok2")

    # Cadre pour le compteur en haut, aligné à gauche
    top_frame = tk.Frame(root, bg="gray")
    top_frame.pack(anchor="w", pady=(outer_padding, 10), padx=outer_padding)

    # Compteur en haut
    counter_label_top = tk.Label(top_frame, text="10", bg="gray", fg="black", font=("Arial", 20))
    counter_label_top.pack(side="left")

    # Rectangle orange en haut
    rectangle_top = tk.Label(top_frame, width=10, bg="orange")
    rectangle_top.pack(side="left", padx=(10, 0))
    rectangle_top.config(height=1, pady=1)
    canvas_haut = tk.Canvas(top_frame, width=35, height=30, bg="gray", highlightthickness=0)
    canvas_haut.pack()
    rond_haut = canvas_haut.create_oval(15, 10, 30, 25, fill="gray", outline="gray")

    # Cadre pour la grille
    frame = tk.Frame(root, padx=outer_padding, pady=outer_padding, bg="gray")
    frame.pack()

    # Canvas pour dessiner la grille et les lignes
    canvas = tk.Canvas(frame, width=cols * (cell_size + padding), height=rows * (cell_size + padding), bg="gray",
                       highlightthickness=0)
    canvas.grid(row=0, column=0)

    # Input pour jouer
    input_joueur = tk.Frame(frame, padx=outer_padding, pady=outer_padding, bg="gray")
    input_joueur.grid(row=0, column=1)
    v1 = tk.BooleanVar()
    checkbox = tk.Checkbutton(input_joueur, text='Horizontal?', variable=v1, onvalue=1, offvalue=0, bg="gray")
    checkbox.grid(row=0, column=0)

    v = tk.StringVar()
    entry = tk.Entry(input_joueur, textvariable=v, width=10)
    entry.grid(row=1, column=0)

    # Fonction pour afficher les bonhommes rouge et noir en fct de leur position avec b pour dire si on colorie ou si on efface
    def pions(b: bool):
        if b:
            canvas.itemconfig(cells[loc1], fill="red")
            canvas.itemconfig(cells[loc2], fill="black")
        else:
            canvas.itemconfig(cells[loc1], fill="white")
            canvas.itemconfig(cells[loc2], fill="white")

    # Fonction pour deplacer un bonhomme selon un string: H->haut B->bas ... le reste-> rien
    def deplacer(string: str):
        global loc1, loc2, jeu  # y,x
        match string:
            case "Z":

                if premier_joueur and loc1[0] >= 1 and (loc1[1], loc1[0] - 1) in plateau[(loc1[1], loc1[0])]:
                    pions(False)
                    loc1 = (loc1[0] - 1, loc1[1])
                    pions(True)
                    if loc1[0]==0:
                        jeu=False
                    tour_suivant(False)
                elif (not (premier_joueur)) and loc2[0] >= 1 and (loc2[1], loc2[0] - 1) in plateau[(loc2[1], loc2[0])]:
                    pions(False)
                    loc2 = (loc2[0] - 1, loc2[1])
                    pions(True)
                    tour_suivant(False)
            case "Q":
                if premier_joueur and loc1[1] >= 1 and (loc1[1] - 1, loc1[0]) in plateau[(loc1[1], loc1[0])]:
                    pions(False)
                    loc1 = (loc1[0], loc1[1] - 1)
                    pions(True)
                    tour_suivant(False)
                elif (not (premier_joueur)) and loc2[1] >= 1 and (loc2[1] - 1, loc2[0]) in plateau[(loc2[1], loc2[0])]:

                    pions(False)
                    loc2 = (loc2[0], loc2[1] - 1)
                    pions(True)
                    tour_suivant(False)
            case "D":
                if premier_joueur and loc1[1] <= 7 and (loc1[1] + 1, loc1[0]) in plateau[(loc1[1], loc1[0])]:
                    pions(False)
                    loc1 = (loc1[0], loc1[1] + 1)
                    pions(True)
                    tour_suivant(False)
                elif (not (premier_joueur)) and loc2[1] <= 7 and (loc2[1] + 1, loc2[0]) in plateau[(loc2[1], loc2[0])]:
                    pions(False)
                    loc2 = (loc2[0], loc2[1] + 1)
                    pions(True)
                    tour_suivant(False)
            case "S":
                if premier_joueur and loc1[0] <= 7 and (loc1[1], loc1[0] + 1) in plateau[(loc1[1], loc1[0])]:
                    pions(False)
                    loc1 = (loc1[0] + 1, loc1[1])
                    pions(True)
                    tour_suivant(False)
                elif (not (premier_joueur)) and loc2[0] <= 7 and (loc2[1], loc2[0] + 1) in plateau[(loc2[1], loc2[0])]:
                    pions(False)
                    loc2 = (loc2[0] + 1, loc2[1])
                    pions(True)
                    if loc2[0]==8:
                        jeu=False
                    tour_suivant(False)

            case _:
                print("Erreur9980: string interdit")

    # Fonction pour passer au tour suivant avec b qui indique si on doit decompter ou pas le compteur de barrieres
    def tour_suivant(b: bool):
        global premier_joueur
        premier_joueur = not (premier_joueur)
        if b:
            update_counter(not (premier_joueur))
        if (premier_joueur):
            canvas_bas.itemconfig(rond_bas, fill="green")
            canvas_haut.itemconfig(rond_haut, fill="gray")
        else:
            canvas_bas.itemconfig(rond_bas, fill="gray")
            canvas_haut.itemconfig(rond_haut, fill="green")

        entry.delete(0, tk.END)

    # Fonction qui joue le tour d'une personne suivant l'entry
    def action(event=None):
        global jeu
        if(jeu):
            try:
                tab = [int(i) for i in entry.get().split()]
                aux = 0
                if premier_joueur:
                    aux = nb1
                else:
                    aux = nb2
                if (aux > 0) and (len(tab) == 3) and ((tab[2] == 1) or (tab[2] == 0)) and (tab[0] >= 0) and (
                        tab[0] <= 7) and (
                        tab[1] >= 0) and (tab[1] <= 7):
                    add_line(tab[0], tab[1], tab[2])

            except:
                try:
                    deplacer((entry.get()).upper())
                except Exception as e:
                    print(e)
                    print("Erreur5048")
            if not jeu:
                affichage_fin()

    def callback(event):
        # print("clicked at", event.x, event.y)
        # print("cellule",event.x//54,event.y//54)
        if v1.get():
            aux = str(event.x // 54) + " " + str(event.y // 54) + " 1"
        else:
            aux = str(event.x // 54) + " " + str(event.y // 54) + " 0"
        v.set(aux)

    # Lier la touche "Entrée" pour déclencher `action`
    entry.bind("<Return>", action)

    canvas.bind("<Button-1>", callback)

    # Boucle pour créer une grille de 9x9 avec des labels espacés
    cells = {}
    for i in range(rows):
        for j in range(cols):
            x1 = j * (cell_size + padding)
            y1 = i * (cell_size + padding)
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            cell = canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
            cells[(i, j)] = cell

    # Fonction pour verifier qu'il existe au moins un chemin solution pour chaque joueur
    def existe_sol(case, ord, visités) -> bool:
        global plateau

        if visités is None:
            visités = set()
        if case[1] == ord:
            return True
        visités.add(case)
        for voisin in plateau.get(case):
            if voisin not in visités:
                if existe_sol(voisin, ord, visités):
                    return True

        return False

    # Fonction pour ajouter un trait orange horizontal ou vertical entre deux cellules
    # On lui donne x,y coordonees de la cellule en haut a gauche et h=True si horizontal
    def add_line(x: int, y: int, h=True):
        global plateau, murs, loc1, loc2
        if not (x >= 0 and x <= 7 and y >= 0 and y <= 7):
            print(f"L'emplacement x: {x}, y: {y} est interdit")
        else:
            if h:
                if ((x, y, int(h)) not in murs) and ((x - 1, y, int(h)) not in murs) and (
                        (x + 1, y, int(h)) not in murs) and ((x, y, 1 - int(h)) not in murs):
                    plateau[(x, y)].remove((x, y + 1))
                    plateau[(x, y + 1)].remove((x, y))
                    plateau[(x + 1, y)].remove((x + 1, y + 1))
                    plateau[(x + 1, y + 1)].remove((x + 1, y))
                    # if ((x, y, int(h)) not in murs) and ((x, y - 1, int(h)) not in murs) and ((x, y + 1, int(h)) not in murs) and ((x, y, 1 - int(h)) not in murs):
                    if existe_sol((loc2[1], loc2[0]), 8, None) and existe_sol((loc1[1], loc1[0]), 0, None):
                        # Calculer les coordonnées du trait en fonction des indices des cellules
                        x1 = x * (cell_size + padding)
                        x2 = x1 + 2 * cell_size + padding
                        y1 = y * (cell_size + padding) + cell_size + padding / 2

                        # Dessiner le trait orange
                        canvas.create_line(x1, y1, x2, y1, fill="orange", width=8)

                        murs.add((x, y, int(h)))

                        tour_suivant(True)
                    else:
                        plateau[(x, y)].add((x, y + 1))
                        plateau[(x, y + 1)].add((x, y))
                        plateau[(x + 1, y)].add((x + 1, y + 1))
                        plateau[(x + 1, y + 1)].add((x + 1, y))
                        print(f"L'emplacement x: {x}, y: {y} bloque un des joueurs")
                    """else:
                        print("erreur1230")
                        print(((x, y, int(h)) not in murs))
                        print(((x, y - 1, int(h)) not in murs))
                        print(((x, y + 1, int(h)) not in murs))
                        print(((x, y, 1 - int(h)) not in murs))"""
                else:
                    print(f"L'emplacement x: {x}, y: {y} est occupé par un autre mur")
            else:
                if ((x, y, int(h)) not in murs) and ((x, y - 1, int(h)) not in murs) and (
                        (x, y + 1, int(h)) not in murs) and ((x, y, 1 - int(h)) not in murs):
                    plateau[(x, y)].remove((x + 1, y))
                    plateau[(x + 1, y)].remove((x, y))
                    plateau[(x + 1, y + 1)].remove((x, y + 1))
                    plateau[(x, y + 1)].remove((x + 1, y + 1))
                    if existe_sol((loc2[1], loc2[0]), 8, None) and existe_sol((loc1[1], loc1[0]), 0, None):
                        # Calculer les coordonnées du trait en fonction des indices des cellules
                        x1 = x * (cell_size + padding) + cell_size + padding / 2
                        y1 = y * (cell_size + padding)
                        y2 = y1 + 2 * cell_size + padding
                        # Dessiner le trait orange
                        canvas.create_line(x1, y1, x1, y2, fill="orange", width=8)

                        murs.add((x, y, int(h)))
                        tour_suivant(True)
                    else:
                        plateau[(x, y)].add((x + 1, y))
                        plateau[(x + 1, y)].add((x, y))
                        plateau[(x + 1, y + 1)].add((x, y + 1))
                        plateau[(x, y + 1)].add((x + 1, y + 1))
                        print(f"L'emplacement x: {x}, y: {y} bloque un des joueurs")
                else:
                    print(f"L'emplacement x: {x}, y: {y} est occupé par un autre mur")

    # Exemple d'ajout de trait horizontal entre deux cellules de la grille
    # add_horizontal_line(6, 4, 1)

    def affichage_fin():
        popup = tk.Toplevel(root)
        global loc1,loc2
        if loc1[0]==0:
            popup.title("ROUGE à gagné la partie")
        else:
            popup.title("NOIR à gagné la partie")

        # Charger et redimensionner l'image

        image = tk.PhotoImage(file="photos/"+str(random.randint(0,9))+".png")
        #image = image.resize((300, 300), Image.ANTIALIAS)  # Redimensionner si nécessaire
        #photo = tk.PhotoImage(image)

        # Afficher l'image dans un Label
        label = tk.Label(popup, image=image)
        label.image = image  # Important pour garder une référence de l'image
        label.pack()

    # Cadre pour le compteur en bas, aligné à gauche
    bottom_frame = tk.Frame(root, bg="gray")
    bottom_frame.pack(anchor="w", pady=(10, outer_padding), padx=outer_padding)

    # Compteur en bas
    counter_label_bottom = tk.Label(bottom_frame, text="10", bg="gray", fg="black", font=("Arial", 20))
    counter_label_bottom.pack(side="left")

    # Rectangle orange en bas avec hauteur réduite
    rectangle_bottom = tk.Label(bottom_frame, width=10, bg="orange")
    rectangle_bottom.pack(side="left", padx=(10, 0))
    rectangle_bottom.config(height=1, pady=1)
    canvas_bas = tk.Canvas(bottom_frame, width=35, height=30, bg="gray", highlightthickness=0)
    canvas_bas.pack()
    rond_bas = canvas_bas.create_oval(15, 10, 30, 25, fill="green", outline="gray")

    # On affiche les pions de depart
    pions(True)

    # Démarrer la boucle principale
    root.mainloop()


# Appeler la fonction pour afficher la grille
create_grid()
