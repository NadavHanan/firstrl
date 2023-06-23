from ml_gametry import CustomEnv
from stable_baselines3 import PPO
import os

models_dir = "models/PPO"
logdir = "logs"
"""
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)
"""
env = CustomEnv()
#model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)
#model.learn(total_timesteps=100000)

model_path = f"{models_dir}/990000.zip"
model = PPO.load(model_path, env=env)
"""
TIMESTEPS = 10000
for i in range(100):
  model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
  model.save(f"{models_dir}/{TIMESTEPS*i}")
"""

obs = env.reset()
for i in range(500):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
      obs = env.reset()

