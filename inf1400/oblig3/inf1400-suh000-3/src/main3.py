import pygame
from pygame import Vector2
import sys
import math

from config import *


def main():
    
    #Initialising pygame 
    pygame.init()
    
    #Display
    pygame.display.set_caption("Oblig 3: Mayhem Clone")
    
    #Classes
    class spaceship(pygame.sprite.Sprite):
        """contains the properties of the spaceship class"""
        def __init__(self, image, position_vector):
            super().__init__()
            self.image = image
            self.position_vector = position_vector
            self.heading = Vector2(0,0)
            self.velocity_vector = Vector2(0,0)
            self.acceleration_vector = Vector2(0,0)
            self.thrust = 0
            self.thrust_vector = Vector2(0,0)
            self.gravity = GRAVITY        
            self.gravity_heading = Vector2(0, 1)
            self.fuel_percentage = FUEL
            self.score = 0       
            self.angle = 0                      #heading in degrees
            self.angle_speed = 3
            self.max_thrust = 0.07       
            self.original_image = self.image    #Storing a copy of the original image to use for rotation       
            self.rect = self.image.get_rect() 
            self.rect.center = self.position_vector
        
                        
        def update(self):
            """updates spaceship position, speed and orientation"""
            #converting from angle in degrees to coordinates in the unit circle
            self.heading = Vector2(math.cos((self.angle+270)*(math.pi/180)), math.sin((self.angle+90)*(math.pi/180)))
            
            #max thrust
            if self.thrust <= -self.max_thrust:
                self.thrust = -self.max_thrust       
             
            #combining thrust and gravity to create acceleration vector
            self.thrust_vector = self.thrust * self.heading        
            self.gravity_vector = self.gravity * self.gravity_heading        
            self.acceleration_vector =  self.thrust_vector + self.gravity_vector  #negative thrust == upwards
            
            #adding the acceleration to the velocity vector
            self.velocity_vector += self.acceleration_vector 
            
            #adding the velocity to the position vector
            self.position_vector += self.velocity_vector
            
            #updating the surface rectangle center with the new position
            self.rect.center = self.position_vector
            
            
            #rotate player 1
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                spaceship1.rotate(COUNTERCLOCKWISE) 
                spaceship1.angle += spaceship1.angle_speed
                
            if pressed[pygame.K_RIGHT]:
                spaceship1.rotate(CLOCKWISE) 
                spaceship1.angle -= spaceship1.angle_speed  
            
            #rotate player 2
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_a]:
                spaceship2.rotate(COUNTERCLOCKWISE) 
                spaceship2.angle += spaceship2.angle_speed
                
            if pressed[pygame.K_d]:
                spaceship2.rotate(CLOCKWISE) 
                spaceship2.angle -= spaceship2.angle_speed
                   
                
            #shoot player 1        
            if pressed[pygame.K_SPACE]:
                bullets_spaceship1_group.add(Bullet(spaceship1.position_vector, spaceship1.heading))
            
            #shoot player 2    
            if pressed[pygame.K_LCTRL]:
                bullets_spaceship2_group.add(Bullet(spaceship2.position_vector, spaceship2.heading))     
                
            #gravity
            if self.position_vector.y < 678:
                self.gravity = GRAVITY
                self.score += 0.1
                
            #refuel base1
            if self.position_vector.y < 685 and self.position_vector.y > 678 and self.position_vector.x < 945 and self.position_vector.x > 855 and self.angle > -30 and self.angle < 30:
                self.refuel()
     
            #refuel base2
            if self.position_vector.y < 685 and self.position_vector.y > 678 and self.position_vector.x < 145 and self.position_vector.x > 55 and self.angle > -30 and self.angle < 30:
                self.refuel()
                
     
        def rotate(self, direction_rotation):   
            """rotate image with direction"""    
            #making sure angle is within -360 to 360 degrees
            if self.angle > 360 or self.angle == 360:
                self.angle -= 360
            if self.angle < -360 or self.angle == -360:
                self.angle += 360
            
            #rotation spaceship
            if direction_rotation == 1:  #Counterclockwise rotation
                self.rotated_image = pygame.transform.rotozoom(self.original_image, direction_rotation*(self.angle + self.angle_speed), 1)             
            if direction_rotation == -1: #Clockwise rotation
                self.rotated_image = pygame.transform.rotozoom(self.original_image, (self.angle - self.angle_speed), 1) 
            
            #storing the rotated image
            self.rotated_rectangle = self.rotated_image.get_rect()        
            self.image = self.rotated_image
            self.rect = self.rotated_rectangle       
            self.rect.center = self.position_vector
            
            
        def reset_rotation(self):
            """resets the rotated image to the original image""" 
            #reseting rotation back to the original image. To be used when spaceship is sent back to spawn.
            self.image = self.original_image
            self.rect = self.original_image.get_rect() 
            self.rect.center = self.position_vector
            
            
        def object_collision(self):   #object collision and crash
            """properties for spaceship, bullets and obsticles interactions"""
            #game window boundaries, top, bottom, left and right 
            if self.position_vector.y < 0 or self.position_vector.y > SCREEN_Y or self.position_vector.x < 0 or self.position_vector.x > SCREEN_X:
                self.back_to_spawn()
                                       
            #collision between obstacles and ship  
            if self.position_vector.y < 560 and self.position_vector.y > 450 and self.position_vector.x < 760 and self.position_vector.x > 650: 
                self.back_to_spawn()
      
            if self.position_vector.y < 360 and self.position_vector.y > 240 and self.position_vector.x < 260 and self.position_vector.x > 140: 
                self.back_to_spawn()
                
            if self.position_vector.y < 210 and self.position_vector.y > 90 and self.position_vector.x < 810 and self.position_vector.x > 690: 
                self.back_to_spawn()
    
            if self.position_vector.y < 410 and self.position_vector.y > 290 and self.position_vector.x < 560 and self.position_vector.x > 440: 
                self.back_to_spawn()
                
            #collision between bullets and ships
            for bullet in bullets_spaceship1_group:
                if spaceship2.position_vector.x < bullet.position.x + 10 and spaceship2.position_vector.x > bullet.position.x - 10 and \
                    spaceship2.position_vector.y < bullet.position.y + 10 and spaceship2.position_vector.y > bullet.position.y - 10:
                    spaceship2.back_to_spawn()
                    #adding score for kill
                    spaceship1.score += 20
     
    
            for bullet in bullets_spaceship2_group:
                if spaceship1.position_vector.x < bullet.position.x + 10 and spaceship1.position_vector.x > bullet.position.x - 10 and \
                    spaceship1.position_vector.y < bullet.position.y + 10 and spaceship1.position_vector.y > bullet.position.y - 10:
                    spaceship1.back_to_spawn()
                    #adding score for kill
                    spaceship2.score += 20
                    
            #collision between spaceships      
            if spaceship1.position_vector.x < spaceship2.position_vector.x + 15 and spaceship1.position_vector.x > spaceship2.position_vector.x - 15 and \
                spaceship1.position_vector.y < spaceship2.position_vector.y + 15 and spaceship1.position_vector.y > spaceship2.position_vector.y - 15:
                    spaceship1.back_to_spawn()
                    spaceship2.back_to_spawn()
                    
                
        def back_to_spawn(self): 
            #to be used everytime a spaceship crashes or gets shot     
            """resets spaceship back to original spawnpoint after interaction"""       
            self.velocity_vector = Vector2(0,0)
            self.acceleration_vector = Vector2(0,0)
            self.angle = 0
            self.gravity = 0
            self.reset_rotation()
            self.fuel_percentage = FUEL 
            if self.position_vector == spaceship1.position_vector:
                self.position_vector = Vector2(900,670)
                #Substracting score due to destroyed
                spaceship1.score -= 10
                
            if self.position_vector == spaceship2.position_vector:
                self.position_vector = Vector2(100,670)
                #Substracting score due to destroyed
                spaceship2.score -= 10        
        
        def refuel(self):
            """sets properties for refuleing on spawnpoint"""
            self.velocity_vector = Vector2(0,0)
            self.acceleration_vector = Vector2(0,0)
            self.reset_rotation()
            self.gravity = 0
            self.fuel_percentage = FUEL
            self.angle = 0
        
        
    class base(pygame.sprite.Sprite):
        """contains properties for base/spawnpoint layout"""
        def __init__(self, position):
            super().__init__()
            self.image = pygame.Surface(BASE_SURFACE_SIZE) #base surface, must be named image for parent class Sprite to work.
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            pygame.draw.rect(self.image, RED, ((0,0), BASE_SURFACE_SIZE))
            self.rect = self.image.get_rect()
            self.rect.center = position
                        
            
    class Bullet(pygame.sprite.Sprite):
        """contains properties for projectile layout"""
        def __init__(self, position, heading):
            super().__init__()
            self.image = pygame.Surface(BULLET_SURFACE_SIZE)
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            pygame.draw.circle(self.image, PINK, BULLET_SURFACE_CENTER , BULLET_RADIUS)
            self.heading = heading
            self.rect = self.image.get_rect()
            self.rect.center = position 
    
            self.position = Vector2(self.rect.center)
            self.bullet_velocity = 15
    
        def update(self):
            """contains position, speed, orientation and interaction-properties for projectile"""
            self.position -= self.heading * self.bullet_velocity
            self.rect.center = self.position
            
            #Remove bullet objects if outside display            
            if not pygame.display.get_surface().get_rect().contains(self.rect):
                self.kill()
          
            #Remove bullet objects if collision between bullets and obstacles                
            if self.position.y < 550 and self.position.y > 450 and self.position.x < 750 and self.position.x > 650:
                for bullets in bullets_spaceship1_group:
                    self.kill()
                for bullets in bullets_spaceship2_group:
                    self.kill()
            
            if self.position.y < 350 and self.position.y > 250 and self.position.x < 250 and self.position.x > 150:
                for bullets in bullets_spaceship1_group:
                    self.kill()
                for bullets in bullets_spaceship2_group:
                    self.kill()
                  
            if self.position.y < 200 and self.position.y > 100 and self.position.x < 800 and self.position.x > 700:
                for bullets in bullets_spaceship1_group:
                    self.kill()
                for bullets in bullets_spaceship2_group:
                    self.kill()
            
            if self.position.y < 400 and self.position.y > 300 and self.position.x < 550 and self.position.x > 450:
                for bullets in bullets_spaceship1_group:
                    self.kill()
                for bullets in bullets_spaceship2_group:
                    self.kill()
                  
            
    class obstacle(pygame.sprite.Sprite):
        """contains properties for visualisation, position and size of obstacles"""
        def __init__(self, pos_obstacles):
            super().__init__()
            self.image = pygame.Surface(OBSTACLE_SIZE)
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            pygame.draw.rect(self.image, DARK_BLUE, ((0,0), OBSTACLE_SIZE))
            self.rect = self.image.get_rect()
            self.rect.center = pos_obstacles
    #end classes
    
    
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
    
    #Obstacles
    obstacle_group = pygame.sprite.Group()
    obstacle_group.add(obstacle(Vector2(POSITION_1)))
    obstacle_group.add(obstacle(Vector2(POSITION_2)))
    obstacle_group.add(obstacle(Vector2(POSITION_3)))
    obstacle_group.add(obstacle(Vector2(POSITION_4)))
    #end creating objects
    
    #Frame rate limit
    clock = pygame.time.Clock()
    
    
    #Game loop
    while GAME_RUNNING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Bye bye")
                pygame.quit()
                sys.exit()  
             
            #Add thrust when keydown
            if event.type == pygame.KEYDOWN:
                #player1
                if event.key == pygame.K_UP: 
                    spaceship1.thrust -= 0.07                
                #player2
                if event.key == pygame.K_w:
                    spaceship2.thrust -= 0.07
            
            #Remove thrust when keyup                
            if event.type == pygame.KEYUP:
                #player1
                if event.key == pygame.K_UP: 
                    spaceship1.thrust = 0
                #player2
                if event.key == pygame.K_w: 
                    spaceship2.thrust = 0
    
            #Remove fuel when thrusting
            if spaceship1.thrust < 0:
                spaceship1.fuel_percentage -= 1
            
            if spaceship2.thrust < 0:
                spaceship2.fuel_percentage -= 1              
                    
                
        #Draw background 
        pygame.draw.rect(SCREEN, WHITE, (0,0,SCREEN_X,SCREEN_Y))
        
        #Draw and handle spaceship        
        spaceship_group.draw(SCREEN)   #Uses image and rect variables to blit inside the sprite class       
        spaceship_group.update()
    
        #Draw and handle bullets
        bullets_spaceship1_group.draw(SCREEN)
        bullets_spaceship1_group.update()
        bullets_spaceship2_group.draw(SCREEN)
        bullets_spaceship2_group.update()
        
        #Draw base
        base_group.draw(SCREEN)
        
        #Initiate collision
        spaceship1.object_collision()
        spaceship2.object_collision()
        
        #Draw obstacles
        obstacle_group.draw(SCREEN)
    
        #Create and blit text
        font = pygame.font.SysFont("showcardgothic", 20) 
        fuel_player_1 = font.render("Fuel level:" + str(int(spaceship1.fuel_percentage)),1,RED) 
        fuel_player_2 = font.render("Fuel level:" + str(int(spaceship2.fuel_percentage)),1,RED)
        SCREEN.blit(fuel_player_1, (SCREEN_X-250,50))
        SCREEN.blit(fuel_player_2, (10,50))
        
        #Create and blit score
        score_player1 = font.render("Player 1 Score:" + str(int(spaceship1.score)),1,BLUE)
        score_player2 = font.render("Player 2 Score:" + str(int(spaceship2.score)),1,BLUE)
        SCREEN.blit(score_player1, (SCREEN_X-250,25))
        SCREEN.blit(score_player2, (10,25))
        
        #Update display
        pygame.display.update()
        
        
if __name__ == "__main__":
    main()