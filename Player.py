class Joueur(object):

    ALPHA=2 #Importance de la position de l'adversaire par rapport à la notre: 1=equiprobable
    PROBA_DEPL=80#probabilité de se déplacer lorsque on joue "aléatoirement"

    # Player
    def __init__(self, humain:bool,J1:bool,V_J1,V_J2):
        """
        Permet de créer un joueur en indiquant s'il est humain, si c'est le premier joueur et les deux dictionnaires des values de positions

        :param humain: Indique si le joueur est un humain ou une IA

        :param J1: Indique si le joueur crée est le 1er joueur

        :param V_J1: Dictionnaire des etats/valeurs de l'IA du J1
        :param V_J2: Dictionnaire des etats/valeurs de l'IA du J2
        """
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
        """
        Fonction éxécutée pour réinitialiser les stats des joueurs


        """
        self.win_nb = 0
        self.lose_nb = 0
        self.rewards = []

    # Fonction pour verifier qu'il existe au moins un chemin solution pour chaque joueur
    def existe_sol(self,case, ord, visites,etat) -> bool:
        """
        Permet de dire si l'emplacement demandé pour la barrière ne bloque pas un joueur dans l'etat donné


        :param case: Indique la position depuis laquelle la recherche de solution est lancée (couple d'entiers)
        :param ord: Indique si on peut atteindre une case d'ordonée ord
        :type ord: int
        :param visites: Utile pour la recherche de solution par parcours en profondeur (ensemble de couples d'entiers)
        :param etat: Indique l'etat dans lequel on se trouve pour chercher la solution
        :return: Renvoie un booléen qui indique si, depuis la position "case", on peut arriver à l'ordonnée "ord"
        :rtype : bool
        """
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
        """
        Permet d'appliquer une action a un etat de jeu


        :param etat: Indique l'etat dans lequel on applique l'action
        :param action: Indique l'action a appliquer
        :return: Renvoie une liste d'entiers qui represente l'etat dans lequel on arriver apres avoir appliquer l'action dans l'etat demandé
        """
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
            if action[2]==0:
                res[action[1]*8 + action[0] + 6]=2
            else:
                res[action[1] * 8 + action[0] + 6] = 1

            if self.J1:
                res[4]-=1
            else:
                res[5]-=1

        return res

    #Fonction qui calcule les actions possibles
    def actions_possibles(self,etat):
        """
        Permet de renvoyer toutes les actions possibles que peut faire une IA suivant sa position (attribut de classe)


        :param etat: Indique l'état dans lequel on cherche les actions possibles
        :return: Renvoie un couple d'ne liste d'actions avec des déplacements ou des emplacements de barrières et le nombre de deplacement possibles
        """
        x1, y1, x2, y2, nb1, nb2 = etat[0],etat[1],etat[2],etat[3],etat[4],etat[5]  # murs:set((x,y,h))
        actions = []
        if self.J1:
            x, y, nb = x1, y1, nb1
        else:
            x, y, nb = x2, y2, nb2
        cpt = 0
        if self.J1:
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
        else:
            # Ajout des actions possibles (cf ligne 418:432 ; fct existe_sol de classe Joueur)
            if y != 8 and (x == 8 or etat[y * 8 + x + 6] != 1) and (x == 0 or etat[y * 8 + x + 5] != 1):
                actions.append("S")
                cpt += 1

            if x != 0 and (y == 8 or etat[y * 8 + x + 5] != 2) and (y == 0 or etat[(y - 1) * 8 + x + 5] != 2):
                actions.append("Q")
                cpt += 1

            if y != 0 and (x == 8 or etat[(y - 1) * 8 + x + 6] != 1) and (x == 0 or etat[(y - 1) * 8 + x + 5] != 1):
                actions.append("Z")
                cpt += 1

            if x != 8 and (y == 8 or etat[y * 8 + x + 6] != 2) and (y == 0 or etat[(y - 1) * 8 + x + 6] != 2):
                actions.append("D")
                cpt += 1

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
        """
        Permet de prendre une action "maitrisée"; avec ce que connait l'IA, elle va prendre ce qui lui semble etre la meilleure option


        :param etat: Indique dans quel etat on se trouve
        :return: Renvoie l'action choisie
        """
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

            if vmax is None or vmax < (myself - Joueur.ALPHA * opponent):
                vmax = (myself - Joueur.ALPHA * opponent) #On cherche a prendre l'action qui maximise la difference des situations
                vi = i
        return actions[vi]


    def play(self, state):
        """
        Permet de faire joueur le tour d'une IA


        :param state: Indique l'etat actuel
        :return: Renvoie l'action que l'IA joue
        """
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
        """
        Permet d'ajouter une transition à l'historique, utile pour la propagation des récompenses (apprentissage)


        :param n_tuple: Contient l'etat precedent, l'action choisie, la recompense gagnée, l'etat d'arrivée
        """
        self.historique.append(n_tuple)
        s, a, r, sp = n_tuple
        self.rewards.append(r)

    def train(self):
        """
        Permet d'entrainer les IA lorsqu'une partie vient de se finir(apprentissage)

        """
        if self.humain:
            return

        # Update the value function if this player is not human
        for transition in reversed(self.historique):
            s, a, r, sp = transition
            t = tuple(s)
            #print(self.J1)
            #print(transition)
            if t not in self.V_self:
                self.V_self[t]=0.
            if r == 0:
                self.V_self[t] = self.V_self[t] + 0.001 * (self.V_self[tuple(sp)] - self.V_self[t])
            else:
                self.V_self[t] = self.V_self[t] + 0.001 * (r - self.V_self[t])

        self.historique = []
