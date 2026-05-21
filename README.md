# Flappy Bird Deep Q-Learning AI 🐦🧠

An AI bot that learns to play Flappy Bird from scratch using Reinforcement Learning (Deep Q-Network).

## 🚀 Overview
This project uses PyTorch and Pygame to build a reinforcement learning agent. The agent starts with zero knowledge of the game and learns to navigate through the pipes by exploring the environment, receiving rewards for passing pipes, and being penalized for crashing.

## 🛠️ Installation

### Requirements
- Python 3.8+
- [PyTorch](https://pytorch.org/) (for the neural network)
- [Pygame-CE](https://pyga.me/) (for the game engine)
- Matplotlib & IPython (for real-time training graphs)

### Setup
1. Clone or download this repository.
2. Install the required dependencies in your terminal:
   ```bash
   pip install pygame-ce torch matplotlib ipython pillow
   ```

## 🎮 How to Run

To start the training loop and watch the AI learn in real-time:
```bash
python agent.py
```
This will open two windows:
- The **Game Window**: Watch the bird play.
- The **Graph Window**: A live updating plot of the agent's scores over time.

> **Note:** You can safely close the application at any time. The bot saves its progress (brain weights, high score, and number of games played) in the `model/` folder and will automatically resume exactly where it left off on your next run!

## 📁 Project Structure

* **`game.py`**: The Flappy Bird environment. It handles the physics, pipe generation, collision detection, and returns the current state and reward to the AI.
* **`agent.py`**: The reinforcement learning loop. It calculates the state, chooses actions (Exploration vs Exploitation), and manages the agent's short-term and long-term memory.
* **`model.py`**: The PyTorch Deep Q-Network (`Linear_QNet`) and the `QTrainer` which implements the Bellman equation to optimize the model.
* **`helper.py`**: Utility script to plot the live training progress.
* **`clean_sprites.py`**: A one-off script used to strip solid backgrounds from the AI-generated PNG sprites to give them true transparency.

## 🧠 How it Works

1. **State**: The AI looks at 4 normalized relative values: horizontal distance to the next pipe, vertical distance to the top pipe gap, vertical distance to the bottom pipe gap, and its current velocity.
2. **Action**: The neural network outputs 2 Q-Values: `[Do Nothing, Flap]`.
3. **Reward**: The environment gives `+10` points for passing a pipe and `-10` points for crashing.
4. **Learning**: Using Experience Replay, the AI constantly retrains its brain on a random batch of its past moves, slowly learning the optimal timing to flap through the pipes.
