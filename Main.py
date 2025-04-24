import tkinter as tk
import random
import threading
import time
import numpy as np
from queue import PriorityQueue

from typing import List






def play(jeu,j1, j2):
    """
    Permet de faire jouer les deux IA ou joueurs humains tour à tour dans l'ordre


    :param jeu: Le plateau de jeu
    :type jeu: Quoridor
    :param j1: Le joueur 1
    :type j1: Joueur
    :param j2: Le joueur 2
    :type j2: Joueur
    """


    joueurs = [j1, j2]
    state=[4,8,4,0,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #print(len(state))
    p = 0
    while jeu.jeu:
        #print(p%2 +1==jeu.J1)
        if jeu.display:
            time.sleep(0.1)
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
    jeu.fermer()



if __name__ == '__main__':
    #game = Quoridor(10)
    #game.start_game()
    NB=10#Nombre de barrières au départ

    V1={}
    V2={}
    j1 = Joueur(humain=False, J1=True,V_J1=V1,V_J2=V2)
    j2 = Joueur(humain=False, J1=False,V_J1=V1,V_J2=V2)
    disp=False

    def display():
        global disp
        while True:
            user_input = input()
            if user_input:
                disp=True


    thread = threading.Thread(target=display)
    thread.start()

    # Entrainement des Agents
    for i in range(10000000):
        if i % 10 == 0:
            j1.eps = max(j1.eps * 0.99999, 0.1)
            j2.eps = max(j2.eps * 0.99999, 0.1)
        #print(disp)
        jeu = Quoridor(NB,display=disp)
        if disp:
            thread = threading.Thread(target=play, args=(jeu,j1,j2))
            thread.start()
            jeu.start_game()
            disp=False
        else:
            play(jeu,j1,j2)
        #play( jeu,j1, j2)
        print(f"fin de la {i} eme partie")
    j1.reset_stat()

    # Jeu contre nous
    #while True:
        #play(game, j1, None, train=False)

