# envs/player_maze.py
import gym
from gym import spaces
import numpy as np

class PlayerMazeEnv(gym.Env):
    """
    player-mode 隨機起點、其他物件固定的 4×4 迷宮
      - goal 固定 (0,0)
      - pit  固定 (0,1)
      - wall 固定 (1,1)
      - player 每次 reset 隨機位置（不可在 goal/pit/wall）
    動作：0=up,1=right,2=down,3=left
    觀測：扁平化 16 維 0~4 (0=empty,1=player,2=goal,3=pit,4=wall)
    獎勵：到 goal +1，進 pit −1，其餘 0；撞牆或出界視為 no-op。
    Episode 在抵達 goal 或 pit 時結束。
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__()
        self.h, self.w = 4, 4
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(0, 4, shape=(self.h*self.w,), dtype=np.int32)
        self.goal_pos = (0, 0)
        self.pit_pos  = (0, 1)
        self.wall_pos = (1, 1)
        self._seed = None
        self.reset()

    def reset(self):
        # 隨機起點（不可在固定物件上）
        while True:
            r = self.np_random.integers(0, self.h)
            c = self.np_random.integers(0, self.w)
            if (r,c) not in {self.goal_pos, self.pit_pos, self.wall_pos}:
                self.player_pos = (r, c)
                break
        return self._get_obs()

    def step(self, action):
        r, c = self.player_pos
        if   action==0: nr, nc = r-1, c
        elif action==1: nr, nc = r,   c+1
        elif action==2: nr, nc = r+1, c
        elif action==3: nr, nc = r,   c-1
        else:            nr, nc = r,   c

        # 檢查邊界與牆
        if 0<=nr<self.h and 0<=nc<self.w and (nr,nc)!=self.wall_pos:
            self.player_pos = (nr,nc)

        done = False
        reward = 0
        if self.player_pos == self.goal_pos:
            reward, done = 1, True
        elif self.player_pos == self.pit_pos:
            reward, done = -1, True

        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        grid = np.zeros((self.h, self.w), dtype=np.int32)
        pr, pc = self.player_pos
        grid[pr,pc] = 1
        grid[self.goal_pos] = 2
        grid[self.pit_pos]  = 3
        grid[self.wall_pos] = 4
        return grid.flatten()

    def render(self, mode='human'):
        print(self._get_obs().reshape(self.h, self.w))

    def seed(self, seed=None):
        self._seed = seed
        self.np_random = np.random.default_rng(seed)
