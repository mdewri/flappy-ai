import torch
import random
import numpy as np
from collections import deque
from game import FlappyGameAI
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 128
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(4, 256, 2)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        # find the next pipe
        next_pipe = None
        if game.pipes:
            pipe_ind = 1 if len(game.pipes) > 1 and game.bird_x > game.pipes[0]['top'].right else 0
            next_pipe = game.pipes[pipe_ind]
        
        if next_pipe:
            dist_x = next_pipe['top'].x - game.bird_x
            top_y = next_pipe['top'].bottom
            bottom_y = next_pipe['bottom'].top
        else:
            dist_x = game.w
            top_y = 0
            bottom_y = game.h

        # Normalized RELATIVE state representation (much easier to learn)
        state = [
            dist_x / game.w,
            (game.bird_y - top_y) / game.h,
            (bottom_y - game.bird_y) / game.h,
            game.bird_vel_y / 10.0
        ]
        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        # Explore more early on, decay over 1000 games
        epsilon_prob = max(0.01, 0.5 - (self.n_games / 1000.0))
        final_move = [0, 0] # [Do nothing, Flap]
        if random.random() < epsilon_prob:
            move = random.randint(0, 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = FlappyGameAI()
    game.fps = 120 # Speed up training visually

    # Try to load existing model
    loaded_games, record = agent.model.load()
    if loaded_games > 0:
        agent.n_games = loaded_games
        print(f"Loaded existing model! Resuming from game {agent.n_games} with record {record}.")

    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save(agent.n_games, record)

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()
