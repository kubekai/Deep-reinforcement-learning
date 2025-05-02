# envs/random_maze.py
import gym
from gym import spaces
import numpy as np

class RandomMazeEnv(gym.Env):
    """
    Random mode: 所有物件 Player/Goal/Pit/Wall 隨機分布
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, size=4, seed=None):
        super().__init__()
        self.size = size
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(0, 4, shape=(size*size,), dtype=np.int32)
        self._rng = np.random.default_rng(seed)
        self.reset()

    def reset(self):
        # 隨機選位置，確保不重疊
        coords = [(i, j) for i in range(self.size) for j in range(self.size)]
        self._rng.shuffle(coords)
        self.player_pos = coords.pop()
        self.goal_pos   = coords.pop()
        self.pit_pos    = coords.pop()
        self.wall_pos   = coords.pop()
        return self._get_obs()

    def step(self, action):
        r, c = self.player_pos
        if action == 0: nr, nc = r-1, c
        elif action == 1: nr, nc = r, c+1
        elif action == 2: nr, nc = r+1, c
        elif action == 3: nr, nc = r, c-1
        else: nr, nc = r, c

        # 邊界與牆檢查
        if 0 <= nr < self.size and 0 <= nc < self.size and (nr, nc) != self.wall_pos:
            self.player_pos = (nr, nc)

        reward, done = 0, False
        if self.player_pos == self.goal_pos:
            reward, done = 1, True
        elif self.player_pos == self.pit_pos:
            reward, done = -1, True

        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        grid = np.zeros((self.size, self.size), dtype=np.int32)
        grid[self.player_pos] = 1
        grid[self.goal_pos]   = 2
        grid[self.pit_pos]    = 3
        grid[self.wall_pos]   = 4
        return grid.flatten()

    def render(self, mode='human'):
        print(self._get_obs().reshape(self.size, self.size))