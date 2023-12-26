
import pygame
import time 
import random
from os import path
import sys

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 0, 255)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("raining cats and fish!!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y,color):
    font = pygame.font.Font(font_name, size)
    color = color
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newfish():
    m = Fish()
    if player.shield <= 100:
        m.image_orig = random.choice([fish_images_small[0], fish_images_small[1]])  # Green or Blue mob
    else:
        m.image_orig = random.choice([fish_images_small[2], fish_images_small[3]])  # Purple or Yellow mob

    m.image = m.image_orig.copy()

    all_sprites.add(m)
    fish.add(m)

def newbad():
    b = BadFish()
    all_sprites.add(b)
    badfish.add(b)

MAX_CATNIPS = 2
catnip_counter = 0

def newcatnip():
    global catnip_counter
    if len(Catnip) < MAX_CATNIPS:
        c = catnip()
        all_sprites.add(c)
        Catnip.add(c)
        catnip_counter += 1

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 1
    BAR_LENGTH = 400
    BAR_HEIGHT = 15
    fill = pct
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def elapsed(self, duration):
        return pygame.time.get_ticks() - self.start_time > duration 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sizex = 50
        self.sizey = 40
        self.original_image = pygame.transform.scale(player_img, (self.sizex, self.sizey))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 0
        self.lives = 1
        self.catnip_fever_active = False

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.bottom = HEIGHT - 10
        

    def update_image(self):
        old_x = self.rect.x
        old_radius = self.radius
        self.image = pygame.transform.scale(player_img, (self.sizex, self.sizey))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.radius = old_radius + 0.5
        self.rect.bottom = HEIGHT - 10
        if not self.catnip_fever_active:
            old_x = self.rect.x
            old_bottom = self.rect.bottom  # Save the original bottom position
            old_radius = self.radius
            self.image = pygame.transform.scale(player_img, (self.sizex, self.sizey))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = old_x
            self.rect.bottom = old_bottom  # Restore the original bottom position
            self.radius = old_radius + 1


class Fish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(fish_images_small)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(5, 10)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 8)

class BadFish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = bad_fish
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(5, 10)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 8)

class catnip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(catnip_img,(40,60))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(5, 10)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 8)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Raining cats and fish!", 40, WIDTH / 2, HEIGHT / 5, BLACK)
    draw_text(screen, "A hungry stray cat wishes upon a star... ", 15, WIDTH / 2, HEIGHT*1.5 / 5, BLACK)
    draw_text(screen, "'please make fish rain from the sky!!'...And it became True!", 15, WIDTH / 2, HEIGHT*1.7 / 5, BLACK)
    draw_text(screen, "Arrow keys to move the cat.", 15,
              WIDTH / 2, HEIGHT * 2/ 5,BLACK)
    draw_text(screen,"catnips make cat high, and gives 20 point each.(maximum 2)", 15,WIDTH/2,HEIGHT*3/5,BLACK)
    draw_text(screen,"blue/green - 5 points, purlple - 7 points, yellow- 10 points.",15,WIDTH/2,HEIGHT*2.25 /5,BLACK)
    draw_text(screen, "Do not eat the grey rotten fish or you'll die!!",15,WIDTH/2,HEIGHT*2.5 /5,BLACK)
    draw_text(screen, "Press a key to feed the cat", 10, WIDTH / 2, HEIGHT * 4 / 5,GREEN)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_clear_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Game clear!", 40, WIDTH / 2, HEIGHT / 3, BLACK)
    draw_text(screen, "Press a key to play again", 10, WIDTH / 2, HEIGHT * 4 / 5,GREEN)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Load all game graphics
background_big = pygame.image.load(path.join(img_dir, "sky.png")).convert()
background=pygame.transform.scale(background_big, (480, 600))
background_orig=pygame.transform.scale(background_big, (480, 600))
background_rect = background.get_rect()
catnip_b_orig=pygame.image.load(path.join(img_dir, "hypnosis.gif")).convert()
catnip_bg=pygame.transform.scale(catnip_b_orig,(480,600))
catnip_bg.set_alpha(200)
catnip_rect = catnip_bg.get_rect()
player_img = pygame.image.load(path.join(img_dir, "cat.png")).convert()
fish_images = []
fish_images_small=[]
fish_list = ['fish-blue.png','fish-green.png','fish-purple.png','fish-yellow.png']
for img in fish_list:
    fish_images.append(pygame.image.load(path.join(img_dir, img)).convert())
for img in fish_images:
    fish_images_small.append(pygame.transform.scale(img,(40,60)))
bad_fish_big= pygame.image.load(path.join(img_dir,'fish-poison.png')).convert()
bad_fish=pygame.transform.scale(bad_fish_big,(50,60))
catnip_img=pygame.image.load(path.join(img_dir, "catnip.png")).convert()

# Load all game sounds
eat_sounds = pygame.mixer.Sound(path.join(snd_dir,'eat.wav'))
catnip_fever=pygame.mixer.Sound(path.join(snd_dir,'catnip.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'HappyTown.mp3'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
fish = pygame.sprite.Group()
badfish = pygame.sprite.Group()
Catnip = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(7):
    newfish()
for i in range(2):
    newbad()

score = 0
pygame.mixer.music.play(loops=-1)
# Game loop
game_over = True
game_clear= False
running = True
catnip_fever_timer = Timer()

while running:
    if game_over:
        game_over = False
        background = background_orig
        catnip_fever_timer.start_time = 0
        catnip_fever.stop()
        player.catnip_fever_active = False
        show_go_screen()
        all_sprites = pygame.sprite.Group()
        fish = pygame.sprite.Group()
        badfish = pygame.sprite.Group()
        Catnip = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(7):
            newfish()
        for i in range(2):
            newbad()
        score = 0
        if score >= 100:
            newcatnip()

    if game_clear:
        game_clear = False
        background = background_orig
        catnip_fever_timer.start_time = 0
        catnip_fever.stop()
        player.catnip_fever_active = False
        show_clear_screen()
        all_sprites = pygame.sprite.Group()
        fish = pygame.sprite.Group()
        badfish = pygame.sprite.Group()
        Catnip = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(7):
            newfish()
        for i in range(2):
            newbad()
        score = 0
        if score >= 100:
            newcatnip()
    
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if a fish hit the player
    hits = pygame.sprite.spritecollide(player, fish, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.sizex += 1
        player.sizey += 1        
        if hit.image_orig in [fish_images_small[0], fish_images_small[1]]:
            player.shield += 5
        elif hit.image_orig == fish_images_small[2]:
            player.shield += 7
        elif hit.image_orig == fish_images_small[3]:
            player.shield += 10
        if player.shield >= 400:
            game_clear=True
        score += player.shield
        eat_sounds.play()
        player.update_image()
        newfish()
        
    # check to see if a badfish hit the player
    hits = pygame.sprite.spritecollide(player, badfish, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.lives -= 1
        newfish()

    #check if cat ate catnip
    if not game_over:
        hits = pygame.sprite.spritecollide(player,Catnip, True, pygame.sprite.collide_circle)
        for hits in hits:
            if not player.catnip_fever_active:
                background = catnip_bg
                player.radius = int(player.rect.width * .85 / 2)
                player.sizex = 50
                player.sizey = 40
                player.shield += 20
                player.speedx = player.speedx * 2
                catnip_fever_timer.start()
                if player.shield >= 400:
                    game_clear=True
                score += player.shield
                eat_sounds.play()
                catnip_fever.play()
                player.update_image()
                newfish()
            player.catnip_fever_active = True
    
    # check if catnip fever is active
    if player.catnip_fever_active and catnip_fever_timer.elapsed(3000):
        # Reset background and catnip fever timer
        background = background_orig
        catnip_fever_timer.start_time = 0
        catnip_fever.stop()
        player.catnip_fever_active = False

    # if the player ate bad fish and died
    if player.lives == 0:
        # Reset the game state
        background = background_orig
        catnip_fever_timer.start_time = 0
        catnip_fever.stop()
        player.catnip_fever_active = False
        all_sprites = pygame.sprite.Group()
        fish = pygame.sprite.Group()
        badfish = pygame.sprite.Group()
        Catnip = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(7):
            newfish()
        for i in range(2):
            newbad()
        score = 0

    # Check if score is greater than 200 and spawn catnip accordingly
    if score >= 200:
        newcatnip()
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score), 15, WIDTH/2,HEIGHT/2,BLACK)
    draw_text(screen, 'Full', 15, 465, 5,WHITE)
    draw_text(screen, 'Hungry', 15, 23, 5,WHITE)
    draw_shield_bar(screen, 51, 6, player.shield)
    # *after* drawing everything, flip the display
    pygame.display.flip()

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()