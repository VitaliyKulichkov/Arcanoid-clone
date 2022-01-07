import pygame
import random
from random import randrange as rnd
from time import sleep
pygame.init()
pygame.font.init()

# Screen settings
size = width, height = (1200, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Basic Arcanoid (Premitive physics)')

# Fps, combo, lives and score
IsStart = 0
Lives = 3
Score = 0
Combo = 1
clock = pygame.time.Clock()
fps = 60

# Sounds
BounceSNew = pygame.mixer.Sound('data/Sounds/BlockHit.ogg')
BouncePlayerS = pygame.mixer.Sound('data/Sounds/ArcPlateHit.ogg')
BrickDestroyS = pygame.mixer.Sound('data/Sounds/BlockHitBreaking.ogg')

# Function to load sprite images
def load_image(name):
    fullname = 'data' + '/' + name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('Cannot load image: ', name)
        raise SystemExit()

    return image


# Paddle class
class Paddle(pygame.sprite.Sprite):
    image = load_image('Paddle.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(P1)
        self.image = Paddle.image
        self.image = pygame.transform.scale(Paddle.image, (150, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

# Brick class
class Brick(pygame.sprite.Sprite):

    #Loading images for brick
    image = load_image('Bricks/Gray.png')
    Red = load_image('Bricks/Red.png')
    Green = load_image('Bricks/Green.png')
    Blue = load_image('Bricks/Blue.png')
    Orange = load_image('Bricks/Orange.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(Bricks)
        self.image = Brick.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        # Choose color of bricks
        self.colorv = random.randint(1, 5)

        if self.colorv == 1:
            self.image = Brick.image
        elif self.colorv == 2:
            self.image = Brick.Green
        elif self.colorv == 3:
            self.image = Brick.Blue
        elif self.colorv == 4:
            self.image = Brick.Red
        elif self.colorv == 5:
            self.image = Brick.Orange

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

        # Collide the ball and bricks
        if pygame.sprite.spritecollide(self, BallG, False):
            global Combo
            global Score

            Score += 5 * Combo
            Combo += 1
            BounceSNew.play()

            if self.image == Brick.image:
                BrickBlow(self.rect.x, self.rect.y)
                BrickDestroyS.play()
                self.kill()
            else:
                self.image = Brick.image

# Ball class
class Ball(pygame.sprite.Sprite):

    image = load_image('Ball.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(BallG)
        self.image = Ball.image
        #self.image = pygame.transform.scale(Ball.image, (3,3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.rdirb = 0
        self.rdirp = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy) # move the ball

        # IF collide with brick - change opposite direction
        if pygame.sprite.spritecollide(self, Bricks, False):

            BounceSNew.play()

            self.rdirb = random.randint(1, 3)
            if self.rdirb == 1:
                self.vx = self.vx
                self.vy = -self.vy
            elif self.rdirb == 2:
                self.vx = -self.vx
                self.vy = -self.vy
            elif self.rdirb == 3:
                self.vx = -self.vx
                self.vy = self.vy

        # Bounce off the paddle
        if pygame.sprite.spritecollide(self, P1, False):
            global Combo
            BouncePlayerS.play()
            Combo = 1
            self.rdirp = random.randint(1, 2)

            if self.rdirp == 1:
                self.vx = self.vx
                self.vy = -self.vy
            elif self.rdirp == 2:
                self.vx = -self.vx
                self.vy = -self.vy

        # Bounce off the screen
        if self.rect.y <= 0:
            self.vx = self.vx
            self.vy = -self.vy

        if self.rect.x >= 1200 or self.rect.x <= 0:
            self.vx = -self.vx
            self.vy = self.vy

        # The ball flew away of the screen - lose 1 live
        if self.rect.y >= 720:
            self.foul()

    # Function for start the ball
    def go(self):
        global IsStart
        self.vx = -4
        self.vy = -4
        IsStart = 1

    # Function for lose lives
    def foul(self):
        global IsStart
        global Lives
        global Combo
        if Lives > 0:
            self.vx = 0
            self.vy = 0
            self.rect.x = 628
            self.rect.y = 480
            Player.rect.x = 480
            IsStart = 0
            Lives -= 1
            Combo = 1
        elif Lives <= 0:
            self.vx = 0
            self.vy = 0
            self.rect.x = -100
            self.rect.y = -100
            IsStart = 2
            Combo = 1

# Background class
class Background(pygame.sprite.Sprite):

    image = load_image('ArcBG.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Background.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Class destroy bricks
class BrickBlow(pygame.sprite.Sprite):

    image = load_image('BrickBreaking/BlockBrake1.png')

    images = ['BrickBreaking/BlockBrake1.png', 'BrickBreaking/BlockBrake2.png', 'BrickBreaking/BlockBrake3.png',
              'BrickBreaking/BlockBrake4.png', 'BrickBreaking/BlockBrake5.png', 'BrickBreaking/BlockBrake6.png',
              'BrickBreaking/BlockBrake7.png', 'BrickBreaking/BlockBrake8.png', 'BrickBreaking/BlockBrake9.png',
              'BrickBreaking/BlockBrake10.png', 'BrickBreaking/BlockBrake11.png', 'BrickBreaking/BlockBrake12.png',
              'BrickBreaking/BlockBrake13.png', 'BrickBreaking/BlockBrake14.png', 'BrickBreaking/BlockBrake15.png',
              'BrickBreaking/BlockBrake16.png', 'BrickBreaking/BlockBrake17.png', 'BrickBreaking/BlockBrake18.png'
              ]

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = BrickBlow.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animtimer = 1
        self.frame = 0

    def update(self):

        self.preload_image = load_image(BrickBlow.images[self.frame])
        self.image = self.preload_image

        if self.frame < 17:
            self.frame += 1

        if self.frame == 17:
            self.kill()


# Set up game font
GameFont = pygame.font.SysFont('calibri', 30)
ScoreText = GameFont.render('Score: ' + str(Score), 1, (255, 255, 255))
ComboText = GameFont.render('Combo: ' + str(Combo), 1, (255, 255, 255))
LivesText = GameFont.render('Lives: ' + str(Lives), 1, (255, 255, 255))

# Creating special group for check collide
all_sprites = pygame.sprite.Group()
P1 = pygame.sprite.Group()
BallG = pygame.sprite.Group()
Bricks = pygame.sprite.Group()

# Creating objects: paddle, ball and background
BackGroundObj = Background(0, 0)
Player = Paddle(400, 600)
PBall = Ball(628, 550)

# Creating bricks
brk_x, brk_y = 50, 100
for i in range(7):
        for j in range(9):

            Brick(brk_x, brk_y)
            brk_x += 128
        brk_y += 32
        brk_x -= 9 * 128

# Main programm
running = True
while running:

    # Control the paddle
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] and IsStart == 1 and Player.rect.right < 1200:
        Player.rect.x += 10
    if keys[pygame.K_a] and IsStart == 1 and Player.rect.left > 0:
        Player.rect.x -= 10

    # Check all bricks destroyed
    if len(Bricks) <= 0:
        PBall.vx = 0
        PBall.vy = 0
        IsStart = 3

    # Press space for start the game
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and IsStart == 0 and Lives > 0:
            IsStart == 1
            PBall.go()

        if event.type == pygame.QUIT:
            running = False

    # Drawing the objects on the screen
    screen.fill((0, 0, 0))

    ScoreText = GameFont.render('Score: ' + str(Score), 1, (255, 255, 255))
    ComboText = GameFont.render('Combo: ' + str(Combo), 1, (255, 255, 255))

    if Lives > 0 :
        LivesText = GameFont.render('Lives: ' + str(Lives), 1, (255, 255, 255))
    elif Lives <= 0:
        LivesText = GameFont.render('Game Over!', 1, (255, 255, 255))
    elif Lives > 0 and IsStart == 3:
        LivesText = GameFont.render('You Win!', 1, (255, 255, 255))

    for sprite in all_sprites:
        sprite.update()
    all_sprites.draw(screen)
    screen.blit(ScoreText, (20, 20))
    screen.blit(ComboText, (20, 660))
    screen.blit(LivesText, (20, 630))
    pygame.display.flip()
    clock.tick(fps)
