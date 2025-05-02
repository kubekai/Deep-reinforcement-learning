# pl_model.py
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from envs.random_maze import RandomMazeEnv
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

class DQNLightning(pl.LightningModule):
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        lr: float = 1e-3,
        gamma: float = 0.99,
        buffer_size: int = 20000,
        batch_size: int = 64,
        eval_episodes: int = 10
    ):
        super().__init__()
        # save_hyperparameters 將參數存入 self.hparams
        self.save_hyperparameters()

        # Q network
        self.net = nn.Sequential(
            nn.Linear(state_dim, 128), nn.ReLU(),
            nn.Linear(128, 128),       nn.ReLU(),
            nn.Linear(128, action_dim)
        )
        # target network
        self.target_net = nn.Sequential(
            *[layer for layer in self.net]
        )
        self.gamma = gamma

    def forward(self, x):
        return self.net(x)

    def training_step(self, batch, batch_idx):
        states, actions, rewards, next_states, dones = batch
        q = self.net(states).gather(1, actions.long())
        with torch.no_grad():
            max_next = self.target_net(next_states).max(1, keepdim=True)[0]
            target   = rewards + self.gamma * max_next * (1 - dones)
        loss = F.mse_loss(q, target)
        # log both on step and on epoch
        self.log('train_loss_step', loss, on_step=True, on_epoch=False, prog_bar=False)
        self.log('train_loss_epoch', loss, on_step=False, on_epoch=True, prog_bar=True)
        return loss

    def on_train_epoch_end(self):
        # 在每個 epoch 結束後，做一輪簡單的 env 評估，算 avg_reward，並避免無限迴圈
        env = RandomMazeEnv()
        total_reward = 0.0
        max_steps_per_eval = env.size * env.size * 4  # 限制步數，避免無限迴圈
        for _ in range(self.hparams.eval_episodes):
            state = env.reset()
            done = False
            steps = 0
            while not done and steps < max_steps_per_eval:
                tensor_s = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                action = self.net(tensor_s).argmax(dim=1).item()
                state, r, done, _ = env.step(action)
                total_reward += r
                steps += 1
        avg_reward = total_reward / self.hparams.eval_episodes
        self.log('avg_reward', avg_reward, prog_bar=True)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.net.parameters(), lr=self.hparams.lr)
        scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer, step_size=1000, gamma=0.9
        )
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'interval': 'step'
            }
        }

    def train_dataloader(self):
        env = RandomMazeEnv()
        buffer = []
        state = env.reset()
        for _ in range(self.hparams.buffer_size):
            a = env.action_space.sample()
            ns, r, done, _ = env.step(a)
            buffer.append((state, a, r, ns, done))
            state = ns if not done else env.reset()

        states, actions, rewards, next_states, dones = zip(*buffer)
        states      = np.array(states, dtype=np.float32)
        actions     = np.array(actions, dtype=np.int64)
        rewards     = np.array(rewards, dtype=np.float32)
        next_states = np.array(next_states, dtype=np.float32)
        dones       = np.array(dones, dtype=np.float32)

        t_states      = torch.from_numpy(states)
        t_actions     = torch.from_numpy(actions).unsqueeze(1)
        t_rewards     = torch.from_numpy(rewards).unsqueeze(1)
        t_next_states = torch.from_numpy(next_states)
        t_dones       = torch.from_numpy(dones).unsqueeze(1)

        dataset = TensorDataset(
            t_states, t_actions, t_rewards, t_next_states, t_dones
        )
        return DataLoader(
            dataset,
            batch_size=self.hparams.batch_size,
            shuffle=True,
            num_workers=4,
            pin_memory=True
        )

