import pygame
import random
import os

pygame.init()

WIDTH = 400
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

BIRD_WIDTH, BIRD_HEIGHT = 34, 24
PIPE_WIDTH, PIPE_HEIGHT = 52, 320

GRAVITY = 0.5
FLAP_VELOCITY = 8
MAX_VELOCITY = 10
PIPE_VELOCITY = 4
PIPE_GAP = 150

COLLISION_PENALTY = -10
PASS_REWARD = 10

font = pygame.font.Font(pygame.font.get_default_font(), 25)
ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')

def load_image(filename, size):
    try:
        img = pygame.image.load(os.path.join(ASSET_DIR, filename))
        return pygame.transform.scale(img, size)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

BIRD_IMG = load_image('bird.png', (BIRD_WIDTH, BIRD_HEIGHT))
PIPE_IMG = load_image('pipe.png', (PIPE_WIDTH, PIPE_HEIGHT))
BG_IMG = load_image('bg.png', (WIDTH, HEIGHT))

if BIRD_IMG is None:
    BIRD_IMG = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
    BIRD_IMG.fill(YELLOW)
if PIPE_IMG is None:
    PIPE_IMG = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
    PIPE_IMG.fill(GREEN)
if BG_IMG is None:
    BG_IMG = pygame.Surface((WIDTH, HEIGHT))
    BG_IMG.fill(SKY_BLUE)

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
        self.bird_x = int(self.w * 0.2)
        self.bird_y = int(self.h / 2)
        self.bird_vel_y = 0
        self.bird_rect = pygame.Rect(self.bird_x, self.bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        
        self.score = 0
        self.frame_iteration = 0
        
        self.pipes = []
        self.add_pipe(self.w + 100)
        
    def add_pipe(self, x):
        height = random.randint(100, 350)
        top_pipe = pygame.Rect(x, height - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)
        bottom_pipe = pygame.Rect(x, height + PIPE_GAP, PIPE_WIDTH, PIPE_HEIGHT)
        self.pipes.append({'top': top_pipe, 'bottom': bottom_pipe, 'passed': False})

    def play_step(self, action):
        self.frame_iteration += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        if action[1] == 1:
            self.bird_vel_y = -FLAP_VELOCITY
            
        self.bird_vel_y += GRAVITY
        if self.bird_vel_y > MAX_VELOCITY:
            self.bird_vel_y = MAX_VELOCITY
            
        self.bird_y += self.bird_vel_y
        self.bird_rect.y = int(self.bird_y)
        
        for pipe_pair in self.pipes:
            pipe_pair['top'].x -= PIPE_VELOCITY
            pipe_pair['bottom'].x -= PIPE_VELOCITY
            
        if len(self.pipes) > 0 and self.pipes[-1]['top'].x < self.w - 200:
            self.add_pipe(self.w)
            
        if len(self.pipes) > 0 and self.pipes[0]['top'].right < 0:
            self.pipes.pop(0)

        reward = 0
        game_over = False
        if self.is_collision():
            game_over = True
            reward = COLLISION_PENALTY
            return reward, game_over, self.score
            
        for pipe_pair in self.pipes:
            if not pipe_pair['passed'] and pipe_pair['top'].right < self.bird_x:
                self.score += 1
                pipe_pair['passed'] = True
                reward = PASS_REWARD

        self.update_ui()
        if self.fps > 0:
            self.clock.tick(self.fps)
        
        return reward, game_over, self.score
        
    def is_collision(self):
        if self.bird_y > self.h - BIRD_HEIGHT or self.bird_y < 0:
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
