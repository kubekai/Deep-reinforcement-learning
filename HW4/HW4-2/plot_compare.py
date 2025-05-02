import numpy as np
import matplotlib.pyplot as plt

# 載入各算法的 Reward
base     = np.load("base_rewards.npy")
double   = np.load("double_rewards.npy")
dueling  = np.load("dueling_rewards.npy")

episodes = np.arange(1, len(base) + 1)

# 轉成 success binary (1=到達 goal, 0=失敗)
succ_base   = (base   ==  1).astype(float)
succ_double = (double ==  1).astype(float)
succ_dueling= (dueling==  1).astype(float)

# 定義滑動平均函式
def moving_average(x, w):
    return np.convolve(x, np.ones(w)/w, mode='valid')

window = 20
ma_base    = moving_average(base, window)
ma_double  = moving_average(double, window)
ma_dueling = moving_average(dueling, window)
ma_eps     = np.arange(window, len(base) + 1)  # valid 後對應 Episode

# 繪製滑動平均 Reward
plt.figure()
plt.plot(ma_eps, ma_base,    label='Basic DQN')
plt.plot(ma_eps, ma_double,  label='Double DQN')
plt.plot(ma_eps, ma_dueling, label='Dueling DQN')
plt.xlabel('Episode')
plt.ylabel('Moving Average Reward')
plt.title(f'Reward Moving Average (window={window})')
plt.legend()
plt.grid(True)

# 計算累積成功率
cum_base    = np.cumsum(succ_base)    / episodes
cum_double  = np.cumsum(succ_double)  / episodes
cum_dueling = np.cumsum(succ_dueling) / episodes

# 繪製累積成功率
plt.figure()
plt.plot(episodes, cum_base,    label='Basic DQN')
plt.plot(episodes, cum_double,  label='Double DQN')
plt.plot(episodes, cum_dueling, label='Dueling DQN')
plt.xlabel('Episode')
plt.ylabel('Cumulative Success Rate')
plt.title('Cumulative Success Rate Over Episodes')
plt.legend()
plt.grid(True)

plt.show()
