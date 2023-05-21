import pygame
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
BLUE = (0,0,255)

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
        self.score = 0
        
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

        self.position_vector += self.velocity_vector 
        self.rect.center = self.position_vector
        
        
        #rotate
        #player1
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            spaceship1.rotate(counterclockwise) 
            spaceship1.angle += spaceship1.angle_speed
            
        if pressed[pygame.K_RIGHT]:
            spaceship1.rotate(clockwise) 
            spaceship1.angle -= spaceship1.angle_speed  
        
        #player2
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            spaceship2.rotate(counterclockwise) 
            spaceship2.angle += spaceship2.angle_speed
            
        if pressed[pygame.K_d]:
            spaceship2.rotate(clockwise) 
            spaceship2.angle -= spaceship2.angle_speed
        
        
        #Shoot        
        if pressed[pygame.K_SPACE]:
            bullets_spaceship1_group.add(Bullet(spaceship1.position_vector, spaceship1.heading))
            
        if pressed[pygame.K_LCTRL]:
            bullets_spaceship2_group.add(Bullet(spaceship2.position_vector, spaceship2.heading))        
        
        # print("angle", spaceship1.angle)
        # print("heading", spaceship1.heading)
        # print("velocity_vector", spaceship1.velocity_vector)
        # print("position_vector", spaceship1.position_vector)
        # print("thrust", spaceship1.thrust)
        # print("gravity", spaceship1.gravity)
        # print("fuel", spaceship1.fuel_percentage)
        
        # print("angle", spaceship2.angle)
        # print("heading", spaceship2.heading)
        # print("velocity_vector", spaceship2.velocity_vector)
        # print("position_vector", spaceship2.position_vector)
        # print("thrust", spaceship2.thrust)
        # print("gravity", spaceship2.gravity)
        # print("fuel", spaceship2.fuel_percentage)
        
        
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
        #Screen
        #TOP and bottom
        if self.position_vector.y < 0 or self.position_vector.y > SCREEN_Y:
            self.back_to_spawn()
                
        #Left and right
        if self.position_vector.x < 0 or self.position_vector.x > SCREEN_X:
            self.back_to_spawn()
                
            
        #base1
        if self.position_vector.y < 685 and self.position_vector.y > 678 and self.position_vector.x < 945 and self.position_vector.x > 855 and self.angle > -30 and self.angle < 30:
            self.refuel()
 
        #base2
        if self.position_vector.y < 685 and self.position_vector.y > 678 and self.position_vector.x < 145 and self.position_vector.x > 55 and self.angle > -30 and self.angle < 30:
            self.refuel()

        
        #Gravity on
        if self.position_vector.y < 678:
            self.gravity = 0.04
            self.score += 0.1
            

        #objects/maps 
        if self.position_vector.y < 560 and self.position_vector.y > 450 and self.position_vector.x < 760 and self.position_vector.x > 650: 
            self.back_to_spawn()
  
        if self.position_vector.y < 360 and self.position_vector.y > 240 and self.position_vector.x < 260 and self.position_vector.x > 140: 
            self.back_to_spawn()

            
        if self.position_vector.y < 210 and self.position_vector.y > 90 and self.position_vector.x < 810 and self.position_vector.x > 690: 
            self.back_to_spawn()

        if self.position_vector.y < 410 and self.position_vector.y > 290 and self.position_vector.x < 560 and self.position_vector.x > 440: 
            self.back_to_spawn()

            
        #Collision bullets ships
        for bullet in bullets_spaceship1_group:
            if spaceship2.position_vector.x < bullet.pos_shot.x + 10 and spaceship2.position_vector.x > bullet.pos_shot.x - 10 and \
                spaceship2.position_vector.y < bullet.pos_shot.y + 10 and spaceship2.position_vector.y > bullet.pos_shot.y - 10:
                spaceship2.back_to_spawn()
                spaceship1.score += 20
 

        for bullet in bullets_spaceship2_group:
            if spaceship1.position_vector.x < bullet.pos_shot.x + 10 and spaceship1.position_vector.x > bullet.pos_shot.x - 10 and \
                spaceship1.position_vector.y < bullet.pos_shot.y + 10 and spaceship1.position_vector.y > bullet.pos_shot.y - 10:
                spaceship1.back_to_spawn()
                spaceship2.score += 20
                
        #Spaceship collision      
        if spaceship1.position_vector.x < spaceship2.position_vector.x + 15 and spaceship1.position_vector.x > spaceship2.position_vector.x - 15 and \
            spaceship1.position_vector.y < spaceship2.position_vector.y + 15 and spaceship1.position_vector.y > spaceship2.position_vector.y - 15:
                spaceship1.back_to_spawn()
                spaceship2.back_to_spawn()
                
            
    def back_to_spawn(self):             
        self.velocity_vector = Vector2(0,0)
        self.acceleration_vector = Vector2(0,0)
        self.angle = 0
        self.gravity = 0
        self.reset_rotation()
        self.fuel_percentage = 100  
        if self.position_vector == spaceship1.position_vector:
            self.position_vector = Vector2(900,670) 
            spaceship1.score -= 10
        if self.position_vector == spaceship2.position_vector:
            self.position_vector = Vector2(100,670)  
            spaceship2.score -= 10
   
        
    def move():
        pass
    
    def shoot():
        pass
    
    def refuel(self):
        self.velocity_vector = Vector2(0,0)
        self.acceleration_vector = Vector2(0,0)
        self.reset_rotation()
        self.gravity = 0
        self.fuel_percentage = 100
        self.angle = 0
    
class base(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((100,5)) #base surface, må hete image for at sprite skal fungere.
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, RED, ((0,0),(100,5)))
        self.rect = self.image.get_rect()
        self.rect.center = position
                    
        
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
        self.bullet_velocity = 15
        
    
        self.rect = self.image.get_rect() 
        self.rect.center = self.pos_shot 

    def update(self):
        self.pos_shot -= self.direction * self.bullet_velocity
        self.rect.center = self.pos_shot
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
        
        
        if self.pos_shot.y < 550 and self.pos_shot.y > 450 and self.pos_shot.x < 750 and self.pos_shot.x > 650:
            for bullets in bullets_spaceship1_group:
                self.kill()
            for bullets in bullets_spaceship2_group:
                self.kill()
        
        if self.pos_shot.y < 350 and self.pos_shot.y > 250 and self.pos_shot.x < 250 and self.pos_shot.x > 150:
            for bullets in bullets_spaceship1_group:
                self.kill()
            for bullets in bullets_spaceship2_group:
                self.kill()
        
       
        if self.pos_shot.y < 200 and self.pos_shot.y > 100 and self.pos_shot.x < 800 and self.pos_shot.x > 700:
            for bullets in bullets_spaceship1_group:
                self.kill()
            for bullets in bullets_spaceship2_group:
                self.kill()
        

        if self.pos_shot.y < 400 and self.pos_shot.y > 300 and self.pos_shot.x < 550 and self.pos_shot.x > 450:
            for bullets in bullets_spaceship1_group:
                self.kill()
            for bullets in bullets_spaceship2_group:
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
spaceship2 = spaceship(spaceship_image, Vector2(100,670))

spaceship_group.add(spaceship1)
spaceship_group.add(spaceship2)

#Bullets
bullets_spaceship1_group = pygame.sprite.Group() 
bullets_spaceship2_group = pygame.sprite.Group() 

#Base
base_group = pygame.sprite.Group() 
base_group.add(base(Vector2(900,695)))
base_group.add(base(Vector2(100,695)))

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

            #Player1
            if event.key == pygame.K_UP: 
                spaceship1.thrust -= 0.07
                
            #Player2
            if event.key == pygame.K_w:
                spaceship2.thrust -= 0.07
                
         
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP: 
                spaceship1.thrust = 0
            if event.key == pygame.K_w: 
                spaceship2.thrust = 0

        #Check fuel
        if spaceship1.thrust < 0:
            spaceship1.fuel_percentage -= 1
        
        if spaceship2.thrust < 0:
            spaceship2.fuel_percentage -= 1              
                
            
    #Displaying background on the screen (window)
    pygame.draw.rect(SCREEN, WHITE, (0,0,SCREEN_X,SCREEN_Y))
    
    
    
    #Draw spaceship        
    spaceship_group.draw(SCREEN)   #Uses image and rect variables to blit inside the sprite class
    
    
    #Handle spaceship
    spaceship_group.update()

    #Bullets
    bullets_spaceship1_group.draw(SCREEN)
    bullets_spaceship1_group.update()
    bullets_spaceship2_group.draw(SCREEN)
    bullets_spaceship2_group.update()
    
    #Base
    base_group.draw(SCREEN)
    
    
    spaceship1.out_of_bounds()
    spaceship2.out_of_bounds()
    
    #Map
    maps_group.draw(SCREEN)

    #Text
    font = pygame.font.SysFont("showcardgothic", 20) 
    fuel_player_1 = font.render("Fuel level:" + str(spaceship1.fuel_percentage),1,RED) 
    SCREEN.blit(fuel_player_1, (SCREEN_X-250,50))

    fuel_player_2 = font.render("Fuel level:" + str(spaceship2.fuel_percentage),1,RED) 
    SCREEN.blit(fuel_player_2, (10,50))
    
    #Score
    score_player1 = font.render("Player 1 Score:" + str(int(spaceship1.score)),1,BLUE)
    score_player2 = font.render("Player 2 Score:" + str(int(spaceship2.score)),1,BLUE)
    SCREEN.blit(score_player1, (SCREEN_X-250,25))
    SCREEN.blit(score_player2, (10,25))
    

    #Update
    pygame.display.update()