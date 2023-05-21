import pygame
import random
import math
GRAD = math.pi / 180

black = (0,0,0)
#color
grey_gas = (104, 114, 130)

class Config(object):
    fullscreen = True
    width = 1000
    height = 700
    fps = 60

class Player(pygame.sprite.Sprite): #player class
    maxrotate = 180
    down = (pygame.K_DOWN)
    up = (pygame.K_UP)

    def __init__(self, startpos=(102,579), angle=0):
        super().__init__()
        self.pos = list(startpos)
        self.image = pygame.image.load('spaceship.png')
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=startpos)
        self.angle = angle
    
    def update(self, seconds):
        pressedkeys = pygame.key.get_pressed()
        if pressedkeys[self.down]:
            self.angle -= 2
            self.rotate_image()
        if pressedkeys[self.up]:
            self.angle += 2
            self.rotate_image()

    def rotate_image(self):#rotating player image
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
class Bullet(pygame.sprite.Sprite): 
    #This class represents the bullet.
    def __init__(self, pos, angle):
        super().__init__()
        # Rotate the image.
        self.image = pygame.transform.rotate(your_bullet_image, angle)
        self.rect = self.image.get_rect()
        speed = 5  # 5 pixels per frame.
        # Use trigonometry to calculate the velocity.
        self.velocity_x = math.cos(math.radians(-angle)) * speed
        self.velocity_y = math.sin(math.radians(-angle)) * speed
        # Store the actual position in a list or a vector.
        self.pos = list(pos)

    def update(self):
        """ Move the bullet. """
        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y
        # Update the position of the rect as well.
        self.rect.center = self.pos
    
class Mob(pygame.sprite.Sprite):#monster sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('monster.png')
        self.rect = self.image.get_rect()
        self.rect.x = 1400
        self.rect.y = random.randrange(500,600)
        self.speedy = random.randrange(-8, -1)

    def update(self):
        self.rect.x += self.speedy
        if self.rect.x < -100 :
            self.rect.x = 1400
            self.speedy = random.randrange(-8, -1)

player = Player()

mobs = []
for x in range(0,10):
    mob = Mob()
    mobs.append(mob)

print(mobs)

all_sprites_list = pygame.sprite.Group()
allgroup = pygame.sprite.LayeredUpdates()
allgroup.add(player)

for mob in mobs:
    all_sprites_list.add(mob)
    
def main():
    #game 
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()
    screen=pygame.display.set_mode((Config.width, Config.height),         
    pygame.FULLSCREEN)
    background = pygame.image.load('earth.png')
    
    bullet_list = pygame.sprite.Group

    clock = pygame.time.Clock()
    FPS = Config.fps


    mainloop = True
    while mainloop:
        millisecond = clock.tick(Config.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                if event.key == pygame.K_SPACE: #Bullet schiet knop op space
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x
                    bullet.rect.y = player.rect.y
                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)
                    sound.play()
                if event.key == pygame.K_ESCAPE:
                    mailoop = False 


        pygame.display.set_caption("hi")
        allgroup.update(millisecond)
        all_sprites_list.update()
        screen.blit(background, (0,0))
        allgroup.draw(screen)
        all_sprites_list.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
    pygame.quit()