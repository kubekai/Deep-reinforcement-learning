# dqn/agent.py
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from .network       import QNetwork
from .replay_buffer import ReplayBuffer

class DQNAgent:
    def __init__(self, state_dim, action_dim, cfg):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Q 網路與 target 網路
        self.q_net      = QNetwork(state_dim, action_dim).to(self.device)
        self.target_net = QNetwork(state_dim, action_dim).to(self.device)
        self.target_net.load_state_dict(self.q_net.state_dict())

        self.optimizer = optim.Adam(self.q_net.parameters(), lr=cfg['lr'])

        # 切換是否使用 Replay Buffer
        self.use_replay = cfg.get('use_replay', True)
        if self.use_replay:
            self.replay_buffer = ReplayBuffer(cfg['buffer_size'])

        # 其他超參數
        self.gamma             = cfg['gamma']
        self.batch_size        = cfg['batch_size']
        self.epsilon           = cfg['eps_start']
        self.eps_end           = cfg['eps_end']
        self.eps_decay         = cfg['eps_decay']
        self.update_target_steps = cfg['target_update']
        self.learn_step_counter  = 0

    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, self.q_net.out.out_features)
        s = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        return self.q_net(s).argmax().item()

    def decay_epsilon(self):
        self.epsilon = max(self.eps_end, self.epsilon * self.eps_decay)

    def learn(self):
        # 原本的帶 Replay Buffer 更新流程
        if len(self.replay_buffer) < self.batch_size:
            return
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)
        # …（同之前實作：計算 q_values, target, loss, backward）…

    def learn_naive(self, state, action, reward, next_state, done):
        """
        純 Naive DQN：直接用最新一筆 (s,a,r,s',done) 做一次 TD 更新
        """
        s  = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        a  = action
        r  = reward
        ns = torch.FloatTensor(next_state).unsqueeze(0).to(self.device)
        d  = float(done)

        # 當前 Q(s,a)
        q_val = self.q_net(s)[0, a]
        # 下一步 max_a' Q(s',a')
        with torch.no_grad():
            max_next = self.q_net(ns).max(dim=1)[0]
        target = r + (1 - d) * self.gamma * max_next

        loss = nn.MSELoss()(q_val, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # 依舊需要定期更新 target network
        self.learn_step_counter += 1
        if self.learn_step_counter % self.update_target_steps == 0:
            self.target_net.load_state_dict(self.q_net.state_dict())
