# train.py
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import CSVLogger
from envs.random_maze import RandomMazeEnv
from pl_model import DQNLightning

if __name__ == '__main__':
    env = RandomMazeEnv()
    state_dim  = env.observation_space.shape[0]
    action_dim = env.action_space.n

    model = DQNLightning(
        state_dim,
        action_dim,
        lr=1e-3,
        gamma=0.99,
        buffer_size=20000,  # 可以調整
        batch_size=64       # 可以調整
    )

    # 用 CSVLogger 存每次 log 到 logs/dqn_logs
    logger = CSVLogger("logs", name="dqn_logs")
    checkpoint = ModelCheckpoint(monitor='train_loss_epoch', mode='min')
    trainer = pl.Trainer(
        max_steps=20000,
        callbacks=[checkpoint],
        logger=logger,
        gradient_clip_val=1.0,
        log_every_n_steps=100
    )
    trainer.fit(model)
