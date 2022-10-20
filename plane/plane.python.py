import pygame
import random
import os
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((500,600))
running=True
clock = pygame.time.Clock()

background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
# rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
expl_sound = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]

font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf .blit(text_surface, text_rect)

FPS = 60
GREEN= (0,255,0)
BLACK= (0,0,0)
RED= (255,0,0)
YELLOW= (255,255,0)
WHITE= (255,255,255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = 250
        self.rect.bottom = 600 - 10
        self.speedx = 8
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x+=self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x-=self.speedx

        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0,500 - self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)

        
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > 600 or self.rect.left > 500 or self.rect.right < 0:
            self.rect.x = random.randrange(0,500 - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()




all_sprites = pygame.sprite.Group()        
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r= Rock()
    all_sprites.add(r)
    rocks.add(r)
score = 0

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    

    
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        score += hit.radius
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
    
    hits = pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    if hits:
        running = False
    
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score),18,500/2,10)
    
    pygame.display.update()
pygame.quit()