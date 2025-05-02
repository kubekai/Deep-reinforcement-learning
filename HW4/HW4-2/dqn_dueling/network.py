# dqn_dueling/network.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class DuelingQNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.fc1     = nn.Linear(state_dim, hidden_dim)
        # Value stream
        self.fc_val  = nn.Linear(hidden_dim, hidden_dim//2)
        self.val_out = nn.Linear(hidden_dim//2, 1)
        # Advantage stream
        self.fc_adv  = nn.Linear(hidden_dim, hidden_dim//2)
        self.adv_out = nn.Linear(hidden_dim//2, action_dim)

    def forward(self, x):
        x    = F.relu(self.fc1(x))
        val  = F.relu(self.fc_val(x))
        adv  = F.relu(self.fc_adv(x))
        val  = self.val_out(val)
        adv  = self.adv_out(adv)
        # Q = V + (A - mean(A))
        return val + adv - adv.mean(dim=1, keepdim=True)
