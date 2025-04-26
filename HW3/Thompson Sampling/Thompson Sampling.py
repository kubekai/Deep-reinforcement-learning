import numpy as np
import matplotlib.pyplot as plt

# Thompson Sampling Algorithm for Bernoulli Bandits
def run_thompson_sampling(bandit_means, T):
    K = len(bandit_means)
    alpha = np.ones(K)
    beta = np.ones(K)
    cumulative_reward = np.zeros(T)
    instantaneous_reward = np.zeros(T)
    selection_counts = np.zeros((T, K))

    for t in range(T):
        theta = np.random.beta(alpha, beta)
        arm = np.argmax(theta)
        reward = np.random.binomial(1, bandit_means[arm])
        alpha[arm] += reward
        beta[arm] += 1 - reward
        instantaneous_reward[t] = reward
        cumulative_reward[t] = cumulative_reward[t-1] + reward if t > 0 else reward
        if t > 0:
            selection_counts[t] = selection_counts[t-1]
        selection_counts[t, arm] += 1

    return cumulative_reward, instantaneous_reward, selection_counts

# Simulation parameters
bandit_means = [0.2, 0.5, 0.7]
runs = 200
T = 1000
K = len(bandit_means)
optimal_arm = np.argmax(bandit_means)

# Storage arrays
cum_ts = np.zeros((runs, T))
inst_ts = np.zeros((runs, T))
sel_ts = np.zeros((runs, T, K))

# Run multiple simulations
for r in range(runs):
    c, i, s = run_thompson_sampling(bandit_means, T)
    cum_ts[r] = c
    inst_ts[r] = i
    sel_ts[r] = s

# Compute average metrics
avg_cum_ts = np.mean(cum_ts, axis=0)
avg_inst_ts = np.mean(inst_ts, axis=0)
avg_sel_ts = np.mean(sel_ts, axis=0)

# Compute average exploration count (non-optimal selections)
expl_ts = np.sum(avg_sel_ts[:, np.arange(K) != optimal_arm], axis=1)

# Plot: Average Cumulative Reward
plt.figure()
plt.plot(avg_cum_ts)
plt.xlabel('Time Step')
plt.ylabel('Average Cumulative Reward')
plt.title('Thompson Sampling: Average Cumulative Reward')
plt.grid(True)
plt.show()

# Plot: Average Instantaneous Reward
plt.figure()
plt.plot(avg_inst_ts)
plt.xlabel('Time Step')
plt.ylabel('Average Instantaneous Reward')
plt.title('Thompson Sampling: Average Instantaneous Reward')
plt.grid(True)
plt.show()

# Plot: Average Exploration Count
plt.figure()
plt.plot(expl_ts)
plt.xlabel('Time Step')
plt.ylabel('Average Exploration Count (non-optimal selections)')
plt.title('Thompson Sampling: Average Exploration Count')
plt.grid(True)
plt.show()
