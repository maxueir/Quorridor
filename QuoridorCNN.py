import torch.nn as nn


def to_tensor(state):
    """
    Convertion de state vers tensor

    :param state: State qu'on traduit vers un tensor pytorch
    :return: tensor pytorch
    """

    tensor = torch.zeros((9, 9, 9))
    # Canal 0 et 1: Position joueur 1 et 2
    tensor[0, state.p1_pos[1], state.p1_pos[0]] = 1
    tensor[1, state.p2_pos[1], state.p2_pos[0]] = 1

    # Canal 2 et 3: Murs horizontaux et verticaux
    for y in range(8):
        for x in range(8):
            if state.h_walls & (1 << (y * 8 + x)):
                tensor[2, y, x] = 1
            if state.v_walls & (1 << (y * 8 + x)):
                tensor[3, y, x] = 1

    # Canal 4 et 5: Nombre de murs restant normalisé pour joueur 1 et 2
    tensor[4, :, :] = state.p1_walls/10
    tensor[5, :, :] = state.p2_walls/10

    # Canal 6 et 7: Objectifs (lignes à atteindre pour joueur 1 et 2)
    tensor[6, 0, :] = 1
    tensor[7, 8, :] = 1

    # Canal 8: Objectifs (lignes à atteindre pour joueur 1 et 2)
    tensor[8, :, :] = state.player1

    return tensor


class QuoridorCNN(nn.Module):
    def __init__(self, action_size=148):
        super().__init__()


        self.conv_block = nn.Sequential(
            nn.Conv2d(9, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU()
        )

        # Tête de politique (actor) | Choix des actions
        self.actor = nn.Sequential(
            nn.Linear(256 * 4 * 4, 512),
            nn.ReLU(),
            nn.Linear(512, action_size),
            nn.Softmax(dim=-1)  # Probabilités des actions
        )

        # Tête de valeur (critic) | Evaluation de la situation
        self.critic = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)  # Valeur V(s)
        )

    def forward(self, x):
        x = self.conv_block(x)

        #actor
        x_flat = x.view(-1, 256 * 4 * 4)
        action_probs = self.actor(x_flat)

        #critic
        state_value = self.critic(x)

        return action_probs, state_value