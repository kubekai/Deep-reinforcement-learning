# train.py
import argparse
import gym
import numpy as np
from envs.static_maze import StaticMazeEnv
from dqn.agent import DQNAgent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="static")
    parser.add_argument("--episodes", type=int, default=500)
    parser.add_argument(
        "--no-replay",
        action="store_true",
        help="啟用純 Naive DQN（不使用 Experience Replay）"
    )
    args = parser.parse_args()

    # 建立環境
    env = StaticMazeEnv()
    state_dim  = env.observation_space.shape[0]
    action_dim = env.action_space.n

    # 超參數設定
    cfg = {
        'lr':             1e-3,
        'gamma':          0.99,
        'buffer_size':    10000,
        'batch_size':     32,
        'eps_start':      1.0,
        'eps_end':        0.1,
        'eps_decay':      0.995,
        'target_update':  100,
        # 根據 --no-replay 切換
        'use_replay':     not args.no_replay
    }

    agent = DQNAgent(state_dim, action_dim, cfg)

    # 訓練迴圈
    for ep in range(1, args.episodes + 1):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, done, _ = env.step(action)

            if agent.use_replay:
                # 帶 Replay Buffer
                agent.replay_buffer.push(state, action, reward, next_state, done)
                agent.learn()
            else:
                # 純 Naive DQN：一步更新
                agent.learn_naive(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward

        agent.decay_epsilon()
        print(f"Episode {ep:3d} | Reward: {total_reward:5.1f} | Epsilon: {agent.epsilon:.3f}")

    env.close()

if __name__ == "__main__":
    main()
