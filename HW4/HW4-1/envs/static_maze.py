# envs/static_maze.py
import gym
from gym import spaces
import numpy as np

class StaticMazeEnv(gym.Env):
    """
    一個 4×4 的靜態迷宮環境：
      - player 固定在 (0,3)
      - goal   固定在 (0,0)
      - pit    固定在 (0,1)
      - wall   固定在 (1,1)
    動作：0=上, 1=右, 2=下, 3=左
    回傳觀測：扁平化後的 4×4 整數矩陣 (0=空格,1=player,2=goal,3=pit,4=wall)
    獎勵：到 goal +1，掉 pit −1，其餘步驟 0
    Episode 在撞 pit 或抵達 goal 時結束。
    """

    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__()
        self.height = 4
        self.width  = 4

        # 動作空間：4 個方向
        self.action_space = spaces.Discrete(4)
        # 觀測空間：16 維扁平整數向量
        self.observation_space = spaces.Box(
            low=0, high=4,
            shape=(self.height * self.width,),
            dtype=np.int32
        )

        # 初始化各物件位置
        self._init_positions()

    def _init_positions(self):
        self.player_pos = [0, 3]
        self.goal_pos   = [0, 0]
        self.pit_pos    = [0, 1]
        self.wall_pos   = [1, 1]

    def reset(self):
        """重置環境到初始固定配置，並回傳初始觀測"""
        self._init_positions()
        return self._get_obs()

    def step(self, action):
        """執行一步，回傳 (obs, reward, done, info)"""
        r, c = self.player_pos
        # 計算欲移動到的新位置
        if   action == 0: nr, nc = r-1, c     # up
        elif action == 1: nr, nc = r,   c+1   # right
        elif action == 2: nr, nc = r+1, c     # down
        elif action == 3: nr, nc = r,   c-1   # left
        else:              nr, nc = r,   c

        # 如果新位置合法且不是牆，就更新 player_pos
        if 0 <= nr < self.height and 0 <= nc < self.width \
           and [nr, nc] != self.wall_pos:
            self.player_pos = [nr, nc]

        # 判斷獎勵與結束
        done = False
        reward = 0
        if self.player_pos == self.goal_pos:
            reward = 1
            done = True
        elif self.player_pos == self.pit_pos:
            reward = -1
            done = True

        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        """回傳目前環境的扁平化 grid"""
        grid = np.zeros((self.height, self.width), dtype=np.int32)
        grid[self.player_pos[0], self.player_pos[1]] = 1
        grid[self.goal_pos[0],   self.goal_pos[1]]   = 2
        grid[self.pit_pos[0],    self.pit_pos[1]]    = 3
        grid[self.wall_pos[0],   self.wall_pos[1]]   = 4
        return grid.flatten()

    def render(self, mode='human'):
        """在終端印出當前的 4×4 Grid"""
        grid = self._get_obs().reshape(self.height, self.width)
        print(grid)
