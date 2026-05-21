import pygame
import random
import os

pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 25)

# Game constants
WIDTH = 400
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# Load and scale images 
try:
    BIRD_IMG = pygame.image.load(os.path.join(ASSET_DIR, 'bird.png'))
    
    PIPE_IMG = pygame.image.load(os.path.join(ASSET_DIR, 'pipe.png'))
    
    BG_IMG = pygame.image.load(os.path.join(ASSET_DIR, 'bg.png'))
    
    BIRD_IMG = pygame.transform.scale(BIRD_IMG, (34, 24))
    PIPE_IMG = pygame.transform.scale(PIPE_IMG, (52, 320))
    BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Error loading assets: {e}")
    
    BIRD_IMG = pygame.Surface((34, 24))
    BIRD_IMG.fill((255, 255, 0)) 
    PIPE_IMG = pygame.Surface((52, 320))
    PIPE_IMG.fill((0, 255, 0)) 
    BG_IMG = pygame.Surface((WIDTH, HEIGHT))
    BG_IMG.fill((135, 206, 235)) 

class FlappyGameAI:
    def __init__(self, w=WIDTH, h=HEIGHT, fps=FPS):
        self.w = w
        self.h = h
        self.fps = fps
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Flappy Bird AI')
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        # Bird state
        self.bird_x = int(self.w * 0.2)
        self.bird_y = int(self.h / 2)
        self.bird_vel_y = 0
        self.bird_rect = pygame.Rect(self.bird_x, self.bird_y, 34, 24)
        
        # Game state
        self.score = 0
        self.frame_iteration = 0
        
        # Pipes
        self.pipes = []
        self.pipe_vel_x = -4
        self.pipe_gap = 150
        self.add_pipe(self.w + 100)
        
    def add_pipe(self, x):
        height = random.randint(100, 350)
        top_pipe = pygame.Rect(x, height - 320, 52, 320)
        bottom_pipe = pygame.Rect(x, height + self.pipe_gap, 52, 320)
        self.pipes.append({'top': top_pipe, 'bottom': bottom_pipe, 'passed': False})

    def play_step(self, action):
        self.frame_iteration += 1
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        if action[1] == 1:
            self.bird_vel_y = -8 
            
        self.bird_vel_y += 0.5 
        if self.bird_vel_y > 10:
            self.bird_vel_y = 10
            
        self.bird_y += self.bird_vel_y
        self.bird_rect.y = int(self.bird_y)
        
        
        for pipe_pair in self.pipes:
            pipe_pair['top'].x += self.pipe_vel_x
            pipe_pair['bottom'].x += self.pipe_vel_x
            
        
        if len(self.pipes) > 0 and self.pipes[-1]['top'].x < self.w - 200:
            self.add_pipe(self.w)
            
        if len(self.pipes) > 0 and self.pipes[0]['top'].right < 0:
            self.pipes.pop(0)

        
        reward = 0
        game_over = False
        if self.is_collision():
            game_over = True
            reward = -10
            return reward, game_over, self.score
            
        
        for pipe_pair in self.pipes:
            if not pipe_pair['passed'] and pipe_pair['top'].right < self.bird_x:
                self.score += 1
                pipe_pair['passed'] = True
                reward = 10

        
        if not game_over and reward == 0:
            reward = 0

        
        self.update_ui()
        
        if self.fps > 0:
            self.clock.tick(self.fps)
        
        return reward, game_over, self.score
        
    def is_collision(self):
        
        if self.bird_y > self.h - 24 or self.bird_y < 0:
            return True
            
       
        for pipe_pair in self.pipes:
            if self.bird_rect.colliderect(pipe_pair['top']) or self.bird_rect.colliderect(pipe_pair['bottom']):
                return True
                
        return False
        
    def update_ui(self):
        self.display.blit(BG_IMG, (0, 0))
        
        for pipe_pair in self.pipes:
            
            top_pipe_img = pygame.transform.flip(PIPE_IMG, False, True)
            self.display.blit(top_pipe_img, (pipe_pair['top'].x, pipe_pair['top'].y))
            
            self.display.blit(PIPE_IMG, (pipe_pair['bottom'].x, pipe_pair['bottom'].y))
            
        self.display.blit(BIRD_IMG, (self.bird_rect.x, self.bird_rect.y))
        
        text = font.render(f"Score: {self.score}", True, BLACK)
        self.display.blit(text, [10, 10])
        pygame.display.flip()
