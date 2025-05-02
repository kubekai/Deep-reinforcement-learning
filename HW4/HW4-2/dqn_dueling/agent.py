# dqn_dueling/agent.py
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

from .network import DuelingQNetwork

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    def push(self,*args): self.buffer.append(tuple(args))
    def sample(self,bs):
        batch = random.sample(self.buffer, bs)
        return map(np.array, zip(*batch))
    def __len__(self): return len(self.buffer)

class DuelingDQNAgent:
    def __init__(self, state_dim, action_dim, cfg):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.q_net      = DuelingQNetwork(state_dim, action_dim).to(self.device)
        self.target_net = DuelingQNetwork(state_dim, action_dim).to(self.device)
        self.target_net.load_state_dict(self.q_net.state_dict())
        self.opt = optim.Adam(self.q_net.parameters(), lr=cfg['lr'])

        self.replay      = ReplayBuffer(cfg['buffer_size'])
        self.gamma       = cfg['gamma']
        self.batch_size  = cfg['batch_size']
        self.epsilon     = cfg['eps_start']
        self.eps_end     = cfg['eps_end']
        self.eps_decay   = cfg['eps_decay']
        self.update_tgt  = cfg['target_update']
        self.step_cnt    = 0

    def select_action(self, s):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, self.q_net.adv_out.out_features)
        s = torch.FloatTensor(s).unsqueeze(0).to(self.device)
        return self.q_net(s).argmax().item()

    def decay_epsilon(self):
        self.epsilon = max(self.eps_end, self.epsilon * self.eps_decay)

    def learn(self):
        if len(self.replay) < self.batch_size:
            return
        s,a,r,ns,d = self.replay.sample(self.batch_size)
        s   = torch.FloatTensor(s).to(self.device)
        a   = torch.LongTensor(a).unsqueeze(1).to(self.device)
        r   = torch.FloatTensor(r).unsqueeze(1).to(self.device)
        ns  = torch.FloatTensor(ns).to(self.device)
        d   = torch.FloatTensor(d).unsqueeze(1).to(self.device)

        q_val = self.q_net(s).gather(1,a)
        with torch.no_grad():
            q_next = self.target_net(ns).max(1, keepdim=True)[0]
            tgt    = r + (1-d)*self.gamma*q_next

        loss = nn.MSELoss()(q_val, tgt)
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()

        self.step_cnt += 1
        if self.step_cnt % self.update_tgt == 0:
            self.target_net.load_state_dict(self.q_net.state_dict())
