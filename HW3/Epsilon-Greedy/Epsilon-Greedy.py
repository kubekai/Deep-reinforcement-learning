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
# Extended simulation recording selections
# -------------------------
def simulate_with_selection(epsilon, bandit_probs, steps, runs):
    all_selected = np.zeros((runs, steps), dtype=int)
    for run in range(runs):
        Q = np.zeros(K)
        N = np.zeros(K, int)
        for t in range(steps):
            # ε-Greedy action
            if np.random.rand() < epsilon:
                action = np.random.randint(K)
            else:
                action = np.argmax(Q)
            all_selected[run, t] = action
            reward = float(np.random.rand() < bandit_probs[action])
            # Update estimates
            N[action] += 1
            Q[action] += (reward - Q[action]) / N[action]
    return all_selected

# Run extended simulations
selection_data = {
    eps: simulate_with_selection(eps, bandit_probs, steps, runs)
    for eps in epsilons
}

# -------------------------
# Chart 1: Probability of Selecting Optimal Arm Over Time
# -------------------------
optimal_arm = int(np.argmax(bandit_probs))

plt.figure()
for eps in epsilons:
    selected = selection_data[eps]
    prob_opt = np.mean(selected == optimal_arm, axis=0)
    plt.plot(prob_opt, label=f"ε = {eps}")
plt.xlabel("Time Step")
plt.ylabel("P(select optimal arm)")
plt.title("Probability of Selecting Optimal Arm Over Time")
plt.legend()
plt.tight_layout()
plt.show()

# -------------------------
# Chart 2: Average Selection Count per Arm (per run)
# -------------------------
plt.figure()
width = 0.25
positions = np.arange(K)
for idx, eps in enumerate(epsilons):
    selected = selection_data[eps]
    counts = np.bincount(selected.flatten(), minlength=K) / runs
    plt.bar(positions + idx * width, counts, width, label=f"ε = {eps}")
plt.xlabel("Arm")
plt.ylabel("Avg selections per run")
plt.title("Average Selection Count per Arm")
plt.xticks(positions + width, [str(i) for i in range(K)])
plt.legend()
plt.tight_layout()
plt.show()
