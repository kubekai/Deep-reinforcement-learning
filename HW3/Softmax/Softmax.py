import numpy as np
import matplotlib.pyplot as plt

# Softmax (Boltzmann) Algorithm Implementation
def run_softmax(bandit_means, T, tau):
    K = len(bandit_means)
    counts = np.zeros(K)
    rewards = np.zeros(K)
    cumulative_reward = np.zeros(T)
    instantaneous_reward = np.zeros(T)
    selection_counts = np.zeros((T, K))
    
    for t in range(T):
        q_est = rewards / np.maximum(counts, 1)
        exp_q = np.exp(q_est / tau)
        probs = exp_q / np.sum(exp_q)
        arm = np.random.choice(K, p=probs)
        reward = np.random.binomial(1, bandit_means[arm])
        
        counts[arm] += 1
        rewards[arm] += reward
        instantaneous_reward[t] = reward
        cumulative_reward[t] = cumulative_reward[t-1] + reward if t > 0 else reward
        selection_counts[t] = counts.copy()
    
    return cumulative_reward, instantaneous_reward, selection_counts

# Simulation parameters
bandit_means = [0.2, 0.5, 0.7]
runs = 200
T = 1000
tau_list = [0.1, 0.2, 0.5, 1.0]
optimal_arm = np.argmax(bandit_means)

# Storage for averaged results
avg_cum = {}
avg_inst = {}
avg_expl = {}

for tau in tau_list:
    cum_all = np.zeros((runs, T))
    inst_all = np.zeros((runs, T))
    sel_all = np.zeros((runs, T, len(bandit_means)))
    for r in range(runs):
        c, i, s = run_softmax(bandit_means, T, tau)
        cum_all[r] = c
        inst_all[r] = i
        sel_all[r] = s
    avg_cum[tau] = np.mean(cum_all, axis=0)
    avg_inst[tau] = np.mean(inst_all, axis=0)
    expl_counts = np.sum(np.mean(sel_all, axis=0)[:, np.arange(len(bandit_means)) != optimal_arm], axis=1)
    avg_expl[tau] = expl_counts

# Plot: Average Cumulative Reward for different tau
plt.figure()
for tau in tau_list:
    plt.plot(avg_cum[tau], label=f'τ={tau}')
plt.xlabel('Time Step')
plt.ylabel('Average Cumulative Reward')
plt.title('Softmax Comparison: Cumulative Reward')
plt.legend()
plt.grid(True)
plt.show()

# Plot: Average Instantaneous Reward for different tau
plt.figure()
for tau in tau_list:
    plt.plot(avg_inst[tau], label=f'τ={tau}')
plt.xlabel('Time Step')
plt.ylabel('Average Instantaneous Reward')
plt.title('Softmax Comparison: Instantaneous Reward')
plt.legend()
plt.grid(True)
plt.show()

# Plot: Average Exploration Count for different tau
plt.figure()
for tau in tau_list:
    plt.plot(avg_expl[tau], label=f'τ={tau}')
plt.xlabel('Time Step')
plt.ylabel('Average Exploration Count (non-optimal)')
plt.title('Softmax Comparison: Exploration Count')
plt.legend()
plt.grid(True)
plt.show()
