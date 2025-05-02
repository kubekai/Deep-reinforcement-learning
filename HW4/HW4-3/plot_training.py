# plot_training.py
import pandas as pd
import matplotlib.pyplot as plt
import os

# 找到最新的 metrics.csv
logdir = "logs/dqn_logs"
versions = sorted([d for d in os.listdir(logdir) if d.startswith("version_")])
latest = versions[-1]
csv_path = os.path.join(logdir, latest, "metrics.csv")

# 讀入訓練記錄
df = pd.read_csv(csv_path)

#── Figure 1: Step-Level Loss ────────────────────────────
plt.figure(figsize=(8, 4))
plt.scatter(df['step'], df['train_loss_step'], s=2, alpha=0.3, label='loss (step)')
# 100-step 滑動平均
if 'train_loss_step' in df.columns:
    smoothed = df['train_loss_step'].rolling(window=100, min_periods=1).mean()
    plt.plot(df['step'], smoothed, '-', linewidth=1, label='smoothed (100 steps)')
plt.title('Training Loss (Step-Level)')
plt.xlabel('Training Step')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#── Figure 2: Epoch-Level Loss ──────────────────────────
plt.figure(figsize=(8, 4))
plt.plot(df['epoch'], df['train_loss_epoch'], 'o-', label='train_loss_epoch')
plt.title('Training Loss (Epoch-Level)')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#── Figure 3: Average Reward ────────────────────────────
plt.figure(figsize=(8, 4))
plt.plot(df['epoch'], df['avg_reward'], 'o-', color='orange', label='avg_reward')
plt.title('Average Reward (Evaluation)')
plt.xlabel('Epoch')
plt.ylabel('Average Reward')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
