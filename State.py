import numpy as np
from heapq import heappush, heappop

class State:

    def __init__(self,nb_walls1=10,nb_walls2=10,p1_pos=(4, 8),p2_pos=(4, 0),h_walls=0,v_walls=0,player1=True):

        self.p1_pos = p1_pos
        self.p2_pos = p2_pos
        self.p1_walls = nb_walls1
        self.p2_walls = nb_walls2
        self.h_walls = h_walls  # Entier pour bitmap
        self.v_walls = v_walls  # Entier pour bitmap
        self.player1 = player1
        self.jeu=True

    #Surcharge du constructeur pour creer une copie d'un etat
    @classmethod
    def init2(self,state):
        self.p1_pos = state.p1_pos
        self.p2_pos = state.p2_pos
        self.p1_walls = state.p1_walls
        self.p2_walls = state.p2_walls
        self.h_walls = state.h_walls  # Entier pour bitmap
        self.v_walls = state.v_walls  # Entier pour bitmap
        self.player1 = state.player1
        self.jeu=True

    #Redefinition de la méthode print
    def __str__(self):
        return f"{self.p1_pos} {self.p2_pos} {self.p1_walls} {self.p2_walls} {self.h_walls} {self.v_walls} {self.player1}"

    #Redefinition de la méthode de hash
    def __hash__(self):
        return hash((self.p1_pos, self.p2_pos,self.p1_walls,self.p2_walls, self.h_walls, self.v_walls))

    #Redefinition de la methode de comparaison
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (
                self.p1_pos == other.p1_pos and
                self.p2_pos == other.p2_pos and
                self.p1_walls == other.p1_walls and
                self.p2_walls == other.p2_walls and
                self.h_walls == other.h_walls and
                self.v_walls == other.v_walls and
                self.player1 == other.player1
        )

    # Applique l'action à l'état courant
    def appliquer_action(self,action):
        """
        Permet d'appliquer une action sur l'état courant

        :param action: permet de préciser de quelle situation on veut partir
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
            if self.player1:
                old_pos = self.p1_pos
            else:
                old_pos = self.p2_pos

            # Calculer la nouvelle position
            dx, dy = moves[action[0]]
            new_pos = (old_pos[0] + dx, old_pos[1] + dy)

            # Mettre à jour la position
            if self.player1:
                self.p1_pos = new_pos
                if new_pos[1]==0:
                    self.jeu=False
            else:
                self.p2_pos = new_pos
                if new_pos[1]==8:
                    self.jeu=False


        else:
            x, y = int(action[0]), int(action[1])
            if action[2]=="0":#Barrière verticale
                self.v_walls=self.v_walls | (1 << (y*8 +x))

            else:#Barrière horizontale
                self.h_walls = self.h_walls | (1 << (y * 8 + x))

            #Actualisation du compteur de barrières
            if self.player1:
                self.p1_walls -= 1
            else:
                self.p2_walls -= 1

        # Changement du joueur actif
        self.player1 = not self.player1


    #Renvoie une liste des actions possibles
    def actions_possibles(self):
        """
        Permet de renvoyer une liste de toutes les actions possibles

        :return: renvoie une liste de string des actions possibles

        """
        ens=({str(i)+str(j)+str(h) for i in range(8) for j in range(8) for h in range(2)})
        aux=[action for action in {"z", "q", "s", "d"} if self.action_valide(action)]
        return aux+[action for action in ens if self.action_valide(action)],len(aux)


    #Indique si l'action est valable dans cet état
    def action_valide(self,action):
        """
        Permet d'indiquer si l'action est valide

        :param action: permet de préciser quelle action on teste
        :type action: str
        :return Booleen indiquant si l'action est valide
        :rtype: bool
        """
        #Si la partie est déjà finie
        if self.p1_pos[1]==0 or self.p2_pos[1]==8:
            return False

        if action in {"z", "q", "s", "d"}:
            if self.player1:
                x, y = self.p1_pos
            else:
                x, y = self.p2_pos

            if (y == 0 and action=="z") or (y == 8 and action=="s") or (x == 0 and action=="q") or (x == 8 and action=="d"):
                return False

            #Correspondance direction/murs possibles
            dict={"z":[(y-1,x),(y-1,x-1)],
                  "q":[(y,x-1),(y-1,x-1)],
                  "s":[(y,x),(y,x-1)],
                  "d":[(y,x),(y-1,x)]}
            for (y2,x2) in dict[action]:
                if 0<=x2<=8 and 0<=y2<=8:
                    aux = y2 * 8 + x2
                    if action=="q" or action=="d":
                        if self.v_walls & (1 << aux):
                            return False
                    else:
                        if self.h_walls & (1 << aux):
                            return False

        else:
            try:
                x, y = int(action[0]), int(action[1])
                h=bool(int(action[2]))
            except Exception:
                return False
            if x>7 or y>7:
                return False
            if (self.player1 and self.p1_walls==0) or ((not self.player1) and self.p2_walls==0):
                return False
            #4 tests de barriere a executer
            if h:
                for i in range(3):
                    if 0<=(x + i - 1)<=7 and self.h_walls & (1 << (y * 8 + x + i - 1)):
                        return False
                if self.v_walls & (1 << (y * 8 + x)):
                    return False

            else:
                for i in range(3):
                    if 0<=(y + i - 1)<=7 and self.v_walls & (1 << ((y + i - 1) * 8 + x)):
                        return False
                if self.h_walls & (1 << (y * 8 + x)):
                    return False

            #Verifier existance solution
            old_h=self.h_walls
            old_v=self.v_walls
            if h:
                self.h_walls = self.h_walls | (1 << (y * 8 + x))
            else:
                self.v_walls = self.v_walls | (1 << (y * 8 + x))
            if not( self.existe_sol(self.p1_pos,0) and self.existe_sol(self.p2_pos,8)):
                self.h_walls = old_h
                self.v_walls = old_v
                return False
            self.h_walls = old_h
            self.v_walls = old_v

        return True

    def depl_valide(self,depart,deplacement):
        """
        Indique si un deplacement est valide depuis une position

        :param depart: couple (x,y)
        :param deplacement: couple de deplacement (direction)
        :return: booleen indiquant si deplacement ok
        """
        x,y=depart
        dx,dy=deplacement

        if dx==0:#Vertical
            if dy==1:#Vers le bas
                if (x!=8 and (self.h_walls & (1 << (y * 8 + x)))) or (x!=0 and (self.h_walls & (1 << (y * 8 + x-1)))):
                    return False
            else:#Vers le haut (-1)
                if (x!=8 and (self.h_walls & (1 << ((y-1) * 8 + x)))) or (x!=0 and (self.h_walls & (1 << ((y-1) * 8 + x-1)))):
                    return False
        else:#Horizontal
            if dx==1:#Vers la droite
                if (y!=8 and (self.v_walls & (1 << (y * 8 + x)))) or (y!=0 and (self.v_walls & (1 << ((y-1) * 8 + x)))):
                    return False
            else:#Vers la gauche (-1)
                if (y!=8 and (self.v_walls & (1 << (y * 8 + x-1)))) or (y!=0 and (self.v_walls & (1 << ((y-1) * 8 + x-1)))):
                    return False
        return True

    #Permet de dire si une solution est toujours valable
    def existe_sol(self, depart, obj_y):
        """
        Indique s'il existe un chemin de depart vers la ligne y en utilisant l'algorithme A*

        :param depart: couple (x,y)
        :param obj_y: Ligne cible
        :return: booleen indiquant si un chemin existe
        """
        x, y = depart
        if y == obj_y:
            return True

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        visited = set()
        heap = []
        heappush(heap, (abs(y - obj_y), x, y)) #On priorise selon la distance entre le y courant et le y objectif

        while heap:
            _, x, y = heappop(heap)
            if y == obj_y:
                return True

            if not((x, y) in visited):
                visited.add((x, y))

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx <= 8 and 0 <= ny <= 8:
                        if self.depl_valide((x, y), (dx, dy)):
                            if (nx, ny) not in visited:
                                priority = abs(ny - obj_y)
                                heappush(heap, (priority, nx, ny))

        return False
