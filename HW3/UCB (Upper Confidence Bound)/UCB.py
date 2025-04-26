import numpy as np
import matplotlib.pyplot as plt

# UCB1 Algorithm Implementation
def run_ucb(bandit_means, T):
    K = len(bandit_means)
    counts = np.zeros(K)            # number of times each arm is selected
    rewards = np.zeros(K)           # total rewards for each arm
    cumulative_reward = np.zeros(T) # cumulative reward sequence
    instantaneous_reward = np.zeros(T) # instantaneous reward sequence
    selection_counts = np.zeros((T, K)) # cumulative selection counts per arm at each step

    # Initialization: select each arm once
    for i in range(K):
        reward = np.random.binomial(1, bandit_means[i])
        counts[i] += 1
        rewards[i] += reward
        instantaneous_reward[i] = reward
        cumulative_reward[i] = (cumulative_reward[i-1] if i > 0 else 0) + reward
        selection_counts[i] = counts.copy()

    # Main loop
    for t in range(K, T):
        avg_reward = rewards / counts
        confidence = np.sqrt((2 * np.log(t + 1)) / counts)
        ucb_values = avg_reward + confidence
        arm = np.argmax(ucb_values)

        reward = np.random.binomial(1, bandit_means[arm])
        counts[arm] += 1
        rewards[arm] += reward
        instantaneous_reward[t] = reward
        cumulative_reward[t] = cumulative_reward[t-1] + reward
        selection_counts[t] = counts.copy()

    return cumulative_reward, instantaneous_reward, selection_counts

# Simulation parameters
bandit_means = [0.2, 0.5, 0.7]
runs = 200
T = 1000
K = len(bandit_means)

# Collect results over multiple runs
cum_rewards = np.zeros((runs, T))
inst_rewards = np.zeros((runs, T))
sel_counts_runs = np.zeros((runs, T, K))

for r in range(runs):
    cum, inst, sel = run_ucb(bandit_means, T)
    cum_rewards[r] = cum
    inst_rewards[r] = inst
    sel_counts_runs[r] = sel

# Compute average metrics
avg_cum_reward = np.mean(cum_rewards, axis=0)
avg_inst_reward = np.mean(inst_rewards, axis=0)
avg_sel_counts = np.mean(sel_counts_runs, axis=0)

# Compute average exploration count (selections of non-optimal arms)
optimal_arm = np.argmax(bandit_means)
exploration_counts = np.sum(avg_sel_counts[:, np.arange(K) != optimal_arm], axis=1)

# Plot: Average Cumulative Reward
plt.figure()
plt.plot(avg_cum_reward)
plt.xlabel('Time Step')
plt.ylabel('Average Cumulative Reward')
plt.title('UCB: Average Cumulative Reward')
plt.grid(True)
plt.show()

# Plot: Average Instantaneous Reward
plt.figure()
plt.plot(avg_inst_reward)
plt.xlabel('Time Step')
plt.ylabel('Average Instantaneous Reward')
plt.title('UCB: Average Instantaneous Reward')
plt.grid(True)
plt.show()

# Plot: Average Exploration Count
plt.figure()
plt.plot(exploration_counts)
plt.xlabel('Time Step')
plt.ylabel('Average Exploration Count (non-optimal selections)')
plt.title('UCB: Average Exploration Count')
plt.grid(True)
plt.show()
