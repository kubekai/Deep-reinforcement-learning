import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Configuration (same as before)
# -------------------------
np.random.seed(42)
K = 10
bandit_probs = np.random.rand(K)    # True Bernoulli probabilities
steps = 1000
runs = 200
epsilons = [0.0, 0.01, 0.1]

# -------------------------
# Extended simulation recording rewards, selections, and exploration flags
# -------------------------
def simulate_detailed(epsilon, bandit_probs, steps, runs):
    all_rewards = np.zeros((runs, steps))
    all_explore = np.zeros((runs, steps), dtype=int)
    for run in range(runs):
        Q = np.zeros(K)
        N = np.zeros(K, int)
        for t in range(steps):
            if np.random.rand() < epsilon:
                # exploration
                action = np.random.randint(K)
                all_explore[run, t] = 1
            else:
                # exploitation
                action = np.argmax(Q)
            reward = float(np.random.rand() < bandit_probs[action])
            all_rewards[run, t] = reward
            N[action] += 1
            Q[action] += (reward - Q[action]) / N[action]
    return all_rewards, all_explore

# Run detailed simulations
data = {eps: simulate_detailed(eps, bandit_probs, steps, runs) for eps in epsilons}

# -------------------------
# Chart 1: Average Cumulative Reward
# -------------------------
plt.figure()
for eps in epsilons:
    rewards, _ = data[eps]
    avg_cum_reward = np.mean(np.cumsum(rewards, axis=1), axis=0)
    plt.plot(avg_cum_reward, label=f"ε = {eps}")
plt.xlabel("Time Step")
plt.ylabel("Average Cumulative Reward")
plt.title("Epsilon-Greedy: Average Cumulative Reward Over Time")
plt.legend()
plt.tight_layout()
plt.show()

# -------------------------
# Chart 2: Average Instantaneous Reward (for comparison)
# -------------------------
plt.figure()
for eps in epsilons:
    rewards, _ = data[eps]
    avg_reward = np.mean(rewards, axis=0)
    plt.plot(avg_reward, label=f"ε = {eps}")
plt.xlabel("Time Step")
plt.ylabel("Average Instantaneous Reward")
plt.title("Epsilon-Greedy: Average Instantaneous Reward Over Time")
plt.legend()
plt.tight_layout()
plt.show()

# -------------------------
# Chart 3: Exploration vs Exploitation Fraction Over Time
# -------------------------
plt.figure()
for eps in epsilons:
    _, explore = data[eps]
    frac_explore = np.mean(explore, axis=0)
    plt.plot(frac_explore, label=f"ε = {eps}")
plt.xlabel("Time Step")
plt.ylabel("Fraction of Exploratory Actions")
plt.title("Exploration Fraction Over Time")
plt.legend()
plt.tight_layout()
plt.show()

# No seaborn; each chart is separate; matplotlib default colors are used.
