import numpy as np
from mpmath import cplot
from State import State
from Interface_jeu import Quoridor
import time
import threading
a={1,2}
b={3,4}
c=a.union(b)
print(c)

print(bool(0))
x=1
y=2
dict={"z":[(y-1,x),(y-1,x-1)],
        "q":[(y,x-1),(y-1,x-1)],
        "s":[(y,x),(y,x-1)],
        "d":[(y,x),(y-1,x)]}
for (y,x) in dict["s"]:
    print(x,y)

y=10

liste=[y-2,2,y*2]
y+=1
print(liste)

def modifier(interface):
    state = State(10)
    #state.p1_pos = (1, 1)
    #state.p2_pos = (5, 5)
    #state.h_walls = 3516514154165154984152
    #state.v_walls = 549641616516515616516516
    state.player1 = True
    interface.setState(state)

    """time.sleep(1)
    interface.updateState("z")
    time.sleep(1)
    interface.updateState("s")
    time.sleep(1)
    interface.updateState("211")"""

state=State(10)
a=Quoridor(state)
thread = threading.Thread(target=modifier,args=(a,))
thread.start()

print("ok" if (5 & (1 << 2)) else "non")

print(a)


"""
voisins = np.ones((9, 9, 4), dtype=bool)  # [haut, droite, bas, gauche]

# Initialiser les bords
voisins[:, 0, 0] = False
voisins[8, :, 1] = False
voisins[:, 8, 2] = False
voisins[0, :, 3] = False

for voisi in voisins[1,2]:
    print(voisi)
cpl=(1,1)
print(cpl+(1,0))
print("ici ",voisins[cpl[0],cpl[1],0]," fin")


str=""
str+="[4,8,4,0,d,d,"
for y in range(8):
    for x in range(8):
        str+="0,"
str+="]"
print(str)

a=[4,8,4,0,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

nombre_base10 = int("0", 36)
print(nombre_base10)
"""

"""
update_counter => a appeler et geré
pions => a appeler et geré
deplacer => geré
tour suivant =>  a appeler et geré
add_line => a appeler et geré
affichage fin => geré
action=> geré a appeler
callback => pas traiter mais a ne pas appeler
existe_sol=> geré a appeler
init_grid => pas gere a ne pas appeler
start_game => geré 
fermer => geré
close =>geré


"""