import pygame
from random import randint
from pygame import Vector2
import sys
import math

#Initialising pygame 
pygame.init()

#Colormap
WHITE = (255,255,255)
RED = (255,25,0)
BLACK = (0,0,0)
PINK = (255,15,219)
DARK_BLUE = (50, 88, 117)

#Display
pygame.display.set_caption("Oblig 3: Mayhem Clone")

#Game window
SCREEN_X = 1000
SCREEN_Y = 700
SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)

#Globals
game_running = True
spaceship_size = (40, 40)
FPS = 60
counterclockwise = 1
clockwise = -1

#Map
object_size_1 = (100, 100)
object_size_2 = (100, 150)

position_1 = (200, 300)
position_2 = (700, 500)
position_3 = (750, 150)
position_4 = (500, 350)

#Images
# spaceship_image = pygame.Surface((60, 60))
# spaceship_image.fill(RED)


spaceship_image = pygame.image.load("spaceship.png")
spaceship_image = spaceship_image.convert_alpha()
spaceship_image = pygame.transform.scale(spaceship_image, spaceship_size)



#class
class spaceship(pygame.sprite.Sprite):
    def __init__(self, image, position_vector):
        super().__init__()
        self.image = image
        self.position_vector = position_vector
        self.start_position_vector = position_vector
        self.heading = Vector2(0,0)
        self.velocity_vector = Vector2(0,0)
        self.acceleration_vector = Vector2(0,0)
        self.thrust = 0
        self.thrust_vector = Vector2(0,0)
        self.gravity = 0.02        
        self.gravity_heading = Vector2(0, 1)
        self.fuel_percentage = 100

        self.angle = 0    #heading
        self.angle_speed = 3
        self.max_thrust = 0.07
        
        self.original_image = self.image
        
        self.rect = self.image.get_rect() 
        self.rect.center = self.position_vector
    
        
    
        
    def update(self):
        #Converting from angle in degrees to coordinates unit circle
        self.heading = Vector2(math.cos((self.angle+270)*(math.pi/180)), math.sin((self.angle+90)*(math.pi/180)))
        
        
        self.thrust_vector = self.thrust * self.heading        
        self.gravity_vector = self.gravity * self.gravity_heading
        
        self.acceleration_vector =  self.thrust_vector + self.gravity_vector  #negative thrust == upwards
        self.velocity_vector += self.acceleration_vector 
        
        #max thrust
        if self.thrust <= -self.max_thrust:
            self.thrust = -self.max_thrust

        self.position_vector += self.velocity_vector # + self.gravity_heading 
        self.rect.center = self.position_vector
        
        
        #rotate
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            spaceship1.rotate(counterclockwise) 
            spaceship1.angle += spaceship1.angle_speed
            
        if pressed[pygame.K_RIGHT]:
            spaceship1.rotate(clockwise) 
            spaceship1.angle -= spaceship1.angle_speed  
        
        #Shoot        
        if pressed[pygame.K_SPACE]:
            bullets_group.add(Bullet(self.position_vector, self.heading))
        
        print("angle", self.angle)
        print("heading", self.heading)
        print("velocity_vector", self.velocity_vector)
        print("position_vector", self.position_vector)
        print("start position_vector", self.start_position_vector)
        print("thrust", self.thrust)
        print("gravity", self.gravity)
        print("fuel", self.fuel_percentage)
        
        
    def rotate(self, direction_rotation):        
        if self.angle > 360 or self.angle == 360:
            self.angle -= 360
        if self.angle < -360 or self.angle == -360:
            self.angle += 360
        if direction_rotation == 1:  #Counterclockwise rotation
            self.rotated_image = pygame.transform.rotozoom(self.original_image, direction_rotation*(self.angle + self.angle_speed), 1)             
        if direction_rotation == -1: #Clockwise rotation
            self.rotated_image = pygame.transform.rotozoom(self.original_image, (self.angle - self.angle_speed), 1) 

        self.rotated_rectangle = self.rotated_image.get_rect() 
        
        
        self.image = self.rotated_image
        self.rect = self.rotated_rectangle
        
        self.rect.center = self.position_vector
        
        
    def reset_rotation(self): 
        self.image = self.original_image
        self.rect = self.original_image.get_rect() 
        self.rect.center = self.position_vector
        
    def out_of_bounds(self):   #destroyed/interaction
        #TOP and bottom
        if self.position_vector.y < 0 or self.position_vector.y > SCREEN_Y:
            self.back_to_spawn()
                
        #Left and right
        if self.position_vector.x < 0 or self.position_vector.x > SCREEN_X:
            self.back_to_spawn()
                     
        #base
        if self.position_vector.y < 685 and self.position_vector.y > 678 and self.position_vector.x < 945 and self.position_vector.x > 855 and self.angle > -30 and self.angle < 30:
            self.velocity_vector = Vector2(0,0)
            self.acceleration_vector = Vector2(0,0)
            for ship in spaceship_group:
                ship.reset_rotation()
            self.gravity = 0
            self.fuel_percentage = 100
            self.angle = 0

        if self.position_vector.y < 678:
            self.gravity = 0.02

        #objects/maps 
        if self.position_vector.y < 560 and self.position_vector.y > 450 and self.position_vector.x < 760 and self.position_vector.x > 650: 
            self.velocity_vector = Vector2(0,0)
            self.acceleration_vector = Vector2(0,0)
            for ship in spaceship_group:
                ship.back_to_spawn()
            self.gravity = 0
            self.fuel_percentage = 100
        
        #(700, 500)

        if self.position_vector.y < 360 and self.position_vector.y > 240 and self.position_vector.x < 260 and self.position_vector.x > 140: 
            self.velocity_vector = Vector2(0,0)
            self.acceleration_vector = Vector2(0,0)
            for ship in spaceship_group:
                ship.back_to_spawn()
            self.gravity = 0
            self.fuel_percentage = 100
            
        #(200, 300)

        if self.position_vector.y < 210 and self.position_vector.y > 90 and self.position_vector.x < 810 and self.position_vector.x > 690: 
            self.velocity_vector = Vector2(0,0)
            self.acceleration_vector = Vector2(0,0)
            for ship in spaceship_group:
                ship.back_to_spawn()
            self.gravity = 0
            self.fuel_percentage = 100

        #(750, 150)

        if self.position_vector.y < 410 and self.position_vector.y > 290 and self.position_vector.x < 560 and self.position_vector.x > 440: 
            self.velocity_vector = Vector2(0,0)
            self.acceleration_vector = Vector2(0,0)
            for ship in spaceship_group:
                ship.back_to_spawn()
            self.gravity = 0
            self.fuel_percentage = 100

        #(500, 350)
            
            
    def back_to_spawn(self):
        self.position_vector = Vector2(900,670)
        self.velocity_vector = Vector2(0,0)
        self.acceleration_vector = Vector2(0,0)
        self.angle = 0
        self.gravity = 0
        for ship in spaceship_group:
            ship.reset_rotation()
        self.fuel_percentage = 100        
            
    def move():
        pass
    
    def shoot():
        pass
    
    def refuel():
        pass
    
class base(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100,5)) #base surface, må hete image for at sprite skal fungere.
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, RED, ((0,0),(100,5)))
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(900,695)
                

        
        
        
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_shot, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, pygame.Color('orange'), (4, 4), 3)
        self.direction = direction
        self.rect = self.image.get_rect(center=pos_shot)
        # self.position = position
        self.pos_shot = pygame.Vector2(self.rect.center)
        self.bullet_velocity = 10
        
    
        self.rect = self.image.get_rect() 
        self.rect.center = self.pos_shot 

    def update(self):
        self.pos_shot -= self.direction * self.bullet_velocity
        self.rect.center = self.pos_shot
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
        
        
        if self.pos_shot.y < 550 and self.pos_shot.y > 450 and self.pos_shot.x < 750 and self.pos_shot.x > 650:
            for bullets in bullets_group:
                self.kill()
        
        if self.pos_shot.y < 350 and self.pos_shot.y > 250 and self.pos_shot.x < 250 and self.pos_shot.x > 150:
            for bullets in bullets_group:
                self.kill()
        
       
        if self.pos_shot.y < 200 and self.pos_shot.y > 100 and self.pos_shot.x < 800 and self.pos_shot.x > 700:
            for bullets in bullets_group:
                self.kill()
        

        if self.pos_shot.y < 400 and self.pos_shot.y > 300 and self.pos_shot.x < 550 and self.pos_shot.x > 450:
            for bullets in bullets_group:
                self.kill()
        
        
class maps(pygame.sprite.Sprite):
    def __init__(self, pos_obstacles):
        super().__init__()
        self.image = pygame.Surface(object_size_1)
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, DARK_BLUE, ((0,0), object_size_1))
        self.rect = self.image.get_rect()
        self.rect.center = pos_obstacles

    
    
#Sound class       
class soundeffects:
    def __init__(self, sound):
        self.sound = pygame.mixer.Sound(sound)
    
    def play(self):
        self.sound.play()
        
    def stop(self):
        self.sound.stop()
        

#sound_HS = soundeffects("Harlem_Shake.wav")



#Creating objects
#Spaceship
spaceship_group = pygame.sprite.Group()

spaceship1 = spaceship(spaceship_image, Vector2(900,670))    #positiv gravity == downwards
#spaceship2 = spaceship(spaceship_image, Vector2(300,300))

spaceship_group.add(spaceship1)
#spaceship_group.add(spaceship2)

#Bullets
bullets_group = pygame.sprite.Group() 

#Base
base_group = pygame.sprite.Group() 
base_group.add(base())

maps_group = pygame.sprite.Group()

maps_group.add(maps(Vector2(position_1)))
maps_group.add(maps(Vector2(position_2)))
maps_group.add(maps(Vector2(position_3)))
maps_group.add(maps(Vector2(position_4)))


#Frame rate limit
clock = pygame.time.Clock()



while game_running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Bye bye")
            pygame.quit()
            sys.exit()  
        if event.type == pygame.KEYDOWN:
            #PLayer1
            # if event.key == pygame.K_LEFT:
            #     spaceship1.rotate(counterclockwise) 
            #     spaceship1.angle += spaceship1.angle_speed
                           
            # if event.key == pygame.K_RIGHT:  
            #     spaceship1.rotate(clockwise)  
            #     spaceship1.angle -= spaceship1.angle_speed   
            
            if event.key == pygame.K_UP: 
                spaceship1.thrust -= 0.07
                
                
            # if event.key == pygame.K_DOWN: 
            #     spaceship1.thrust += 0.1
                
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP: 
                spaceship1.thrust = 0
            #     #PLayer2
            # if event.key == pygame.K_a:
            #     spaceship2.rotate(counterclockwise) 
            #     spaceship2.angle += spaceship2.angle_speed

            # if event.key == pygame.K_d:  
            #     spaceship2.rotate(clockwise)  
            #     spaceship2.angle -= spaceship2.angle_speed

        #Check fuel
        if spaceship1.thrust < 0:
            spaceship1.fuel_percentage -= 1
        
              
                
            
    #Displaying background on the screen (window)
    pygame.draw.rect(SCREEN, WHITE, (0,0,SCREEN_X,SCREEN_Y))
    
    
    
    #Draw spaceship        
    spaceship_group.draw(SCREEN)   #Uses image and rect variables to blit inside the sprite class
    # for ship in spaceship_group:
    #     ship.reset_rotation()
    
    
    #Handle spaceship
    spaceship_group.update()

    #Bullets
    bullets_group.draw(SCREEN)
    bullets_group.update()
    
    #Base
    base_group.draw(SCREEN)
    
    
    spaceship1.out_of_bounds()
    
    #Map
    maps_group.draw(SCREEN)

    #Text
    font_1 = pygame.font.SysFont("showcardgothic", 20) 
    fuel_player_1 = font_1.render("Fuel level:" + str(spaceship1.fuel_percentage),1,RED) 
    SCREEN.blit(fuel_player_1, (SCREEN_X-200,50))


    #Update
    pygame.display.update()