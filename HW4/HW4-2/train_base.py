# train_base.py
import argparse
import numpy as np
from envs.player_maze import PlayerMazeEnv
from dqn_base.agent import DQNAgent

# 全域儲存 list
base_rewards  = []
base_epsilons = []

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--episodes", type=int, default=500)
    args = p.parse_args()

    env = PlayerMazeEnv()
    state_dim, action_dim = env.observation_space.shape[0], env.action_space.n

    cfg = {
        'lr':1e-3, 'gamma':0.99,
        'buffer_size':10000, 'batch_size':32,
        'eps_start':1.0, 'eps_end':0.1, 'eps_decay':0.995,
        'target_update':100
    }
    agent = DQNAgent(state_dim, action_dim, cfg)

    for ep in range(1, args.episodes + 1):
        state = env.reset()
        tot_r, done = 0, False

        while not done:
            a, = agent.select_action(state),
            next_state, r, done, _ = env.step(a)
            agent.replay.push(state, a, r, next_state, done)
            agent.learn()
            state, tot_r = next_state, tot_r + r

        agent.decay_epsilon()
        # 正確地把這一集的 tot_r 加到 list
        base_rewards.append(tot_r)
        base_epsilons.append(agent.epsilon)

        print(f"[Base] Ep{ep:3d} R{tot_r:5.1f} ε{agent.epsilon:.3f}")

    # 訓練結束後存檔
    np.save("base_rewards.npy",  np.array(base_rewards))
    np.save("base_epsilons.npy", np.array(base_epsilons))

    env.close()

if __name__ == "__main__":
    main()
