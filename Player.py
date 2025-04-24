import random
from State import State

class Joueur(object):

    ALPHA=2 #Importance de la position de l'adversaire par rapport à la notre: 1=equiprobable
    PROBA_DEPL=80#probabilité de se déplacer lorsque on joue "aléatoirement"

    def __init__(self,J1:bool,V_J1,V_J2):
        """
        Permet de créer un joueur en indiquant s'il est humain, si c'est le premier joueur et les deux dictionnaires des values de positions

        #:param humain: Indique si le joueur est un humain ou une IA

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
        #self.humain = humain
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


    #Fonction d'exploitation
    def greedy_step(self,state):
        """
        Permet de prendre une action "maitrisée"; avec ce que connait l'IA, elle va prendre ce qui lui semble etre la meilleure option


        :return: Renvoie l'action choisie
        """
        vmax = None
        vi = None

        actions,_ = state.actions_possibles()

        for i in range(len(actions)):
            a = actions[i]
            etat_suivant=State.init2(state)
            etat_suivant.appliquer_action(a)

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


    def play(self,state):
        """
        Permet de faire joueur le tour d'une IA

        :return: Renvoie l'action que l'IA joue
        """
        # Take random action
        if random.uniform(0, 1) < self.eps:
            p = random.randint(0, 100)
            actions,cpt=state.actions_possibles()
            #print(actions)
            #print(cpt)
            if p<Joueur.PROBA_DEPL or cpt==len(actions):
                return actions[random.randint(0, cpt-1)]
            else:
                return actions[random.randint(cpt, len(actions)-1)]
        else:  # Or greedy action
            return self.greedy_step(state)

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
