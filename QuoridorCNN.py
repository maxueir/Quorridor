import torch.nn as nn

class QuoridorCNN(nn.Module):
    def __init__(self):
        super().__init__()

        # Couches convolutives pour traiter la grille
        self.conv1 = nn.Conv2d(5, 32, kernel_size=3, padding=1)  # 5 canaux : joueurs, murs H/V, objectifs
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # Couches pour les murs (branche parallèle)
        self.fc_walls = nn.Linear(64*9*9 + 2, 128)  # +2 pour le compte de murs restants
        # Tête décisionnelle
        self.fc_action = nn.Linear(128, 128)  # 84 déplacements + 64 positions murs