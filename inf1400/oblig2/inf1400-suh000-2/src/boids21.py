import pygame
from pygame import Vector2
from pygame.locals import *
import sys
import random, math, numpy, copy

#################
#     setup     #
#################

pygame.init()

#Window
size = width, height = 1920, 1080
#screen_width = 1920 
#screen_height = 1080

#color picker
navy_blue = (50, 127, 168)
crow_gray = (67, 76, 82)
hoik_red = (245, 66, 99)
obstacles_yellow = (204, 172, 43)



#Game window
screen = pygame.display.set_mode(size) 
background = pygame.Surface(size)
pygame.display.set_caption("Boids") 


borderlimit = 25

#Global
minDistance = float(random.randrange(0, 5))
fps = 60
maxVelocity = 6
hawk_velocity = 7
nudge_var = 0.7
nudge_varh = 1.1
radius_boid = 10
radius_hoik = 9



obstacles_radius = 25
num_obstacles = 3
obstacles_list = []



numBoids = 25
boids = []
numHoiks = 8
hoiks = []

#################
#     class     #
#################

   
    
#Parent class

class bird():
    # sets positional orientation and speed for bird on screen
    def __init__(self):
        self.pos = Vector2(random.randint(0, width), random.randint(0, height))                                 
        self.velocity = Vector2(random.uniform(-maxVelocity, maxVelocity), random.uniform(-maxVelocity, maxVelocity))
        
    # moves object
    def move(self):
        if self.velocity.magnitude() > maxVelocity: 
            self.velocity = self.velocity.normalize() * maxVelocity    
        
        self.pos += self.velocity

    # send object to the opposite side of screen when it reaches max width/height 
    def border(self):
        if self.pos.x < 0:
            self.pos.x = width 
        if self.pos.x > width:
            self.pos.x = 0 
        if self.pos.y < 0:
            self.pos.y = height 
        if self.pos.y > height:
            self.pos.y = 0 
    
    # unsuccessful implementation of obstacles !not working
    def avvoid_obs(self, obstacles):
        
        if self.pos.x == obstacles:
            self.velocity.x *= -1
        if self.pos.y == obstacles:
            self.velocity.y *= -1

        
# chld class
    
class boid(bird):
    
    # draw object
    def update(self):
        position = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(screen, crow_gray, position, radius_boid)
    
    # seperate function
    def separation(self, boids):
        if len(boids) > 0: 
            dir_vec = Vector2(0, 0)                 #reset vector
            for boid in closeBoids:                 # for boid in list
                dir_vec += (boid.pos - self.pos)    # adjust reset vector position between two objects
            
            dir_vec /= len(boids)                   # adjust reset vector on the length og objects
            dir_vec = dir_vec * (-1)                # hard coded adjustment
            
            self.velocity += (dir_vec)              # velocity updated

    
    #move closer to a set of boids
    def cohesion(self, boids):
        if len(boids) > 0:
            
            avg_vel = Vector2(0, 0)                 #reset vector     
            
            for boid in boids:                      # for all boids
                avg_vel += (boid.pos - self.pos)    # adjust reset vector position between two objects
                

            avg_vel /= len(boids)                   # adjust reset vector on the length of objects
            #print("avg_vel: ",avg_vel, "self.velocity:", self.velocity)
            self.velocity += avg_vel                # velocity updated
    
    #align the boids
    def alignment(self, boids):
        if len(boids) > 0:
            avg_pos = Vector2(0, 0)                 #reset vector 
            for boid in boids:                      #for all boids
                avg_pos += boid.velocity        
            
            avg_pos /= len(boids)              # induvidual boid velocity devided by boids in list

            self.velocity += avg_pos                # velocity update

    # adds random change in orientation
    def nudge(self, boids):
        nudge_it = Vector2(random.uniform(-nudge_var, nudge_var), random.uniform(-nudge_var, nudge_var))
        if len(boids) > 0:
            for boid in boids:
                boid.velocity += nudge_it           # adds a random vector nugde in orientation
            
         
class hoik(bird):
    def __init__(self):
        super().__init__()
        self.velocity = Vector2(random.uniform(-hawk_velocity, hawk_velocity), random.uniform(-hawk_velocity, hawk_velocity))
    def move(self):
        super().move()
        if self.velocity.magnitude() > hawk_velocity:           # Gives hoik more speed compered to bird function
             self.velocity += self.velocity *hawk_velocity 
        self.pos += self.velocity /2                            # hard coded speed adjustment

    # draws object 
    def update(self):
        position = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(screen, hoik_red, position, radius_hoik)
    
    # seperate objects
    def separation(self, hoiks):
        if len(hoiks) > 0: 
            dir_vec = Vector2(0, 0)                             #reset vector
            for hoik in hoiks:                                  # for hoiks in list
                dir_vec += (hoik.pos - self.pos)                # adjust reset vector position between two objects (self and other boid)
            
            dir_vec /= len(hoiks)                               # adjust reset vector on the length of objects
            dir_vec = dir_vec * (-1)                            # hard coded adjustment
            
            self.velocity += (dir_vec)                          # velocity update

    
    def alignment(self, hoiks):
        if len(hoiks) > 0:
            avg_pos = Vector2(0, 0)                             # reset vector 
            for hoik in hoiks:                                  # for all hoik in hoiks
                avg_pos += hoik.velocity                         # induvidual boid velocity devided by boids in list
            
            avg_pos /= len(hoiks)                               # induvidual boid velocity devided by boids in list

            self.velocity += avg_pos                            # velocity update

    
    #move closer to a set of boids
    def cohesion(self, hoiks):
        if len(hoiks) > 0:
            
            avg_vel = Vector2(0, 0)
            
            for hoik in hoiks:   
                avg_vel += (hoik.pos - self.pos)    

            avg_vel /= len(hoiks)
            #print("avg_vel: ",avg_vel, "self.velocity:", self.velocity)
            self.velocity += avg_vel                            # velocity update


    def nudge(self, hoiks):
        nudge_it = Vector2(random.uniform(-nudge_varh, nudge_varh), random.uniform(-nudge_varh, nudge_varh))
        if len(hoiks) > 0:
            for hoik in huntteam:
                hoik.velocity += nudge_it *2                       # hardcoded change in nudge

# obstacles class
class obstacles(object):
    def __init__(self):
        self.pos = Vector2(random.randint(0, width), random.randint(0, height))            # given random position
    
    # draws object
    def draw(self):
        position = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(screen, obstacles_yellow, position, obstacles_radius )
        



#################
#     main     #
#################

FPS_clock = pygame.time.Clock()

for i in range(numBoids):        # calls for numbers in list 
    i = boid()                   # object class
    boids.append(i)              # gives the class a list

for i in range(numHoiks):
    i = hoik()
    hoiks.append(i)

for i in range(num_obstacles):
    i = obstacles()
    obstacles_list.append(i)
  

# Main loop
while True:
    FPS_clock.tick(fps)
    for event in pygame.event.get():
        #Quit event
        if event.type == pygame.QUIT:
            print("Bye")
            pygame.quit()
            sys.exit()

    screen.fill(navy_blue)

    for obstacles in obstacles_list:            
        obstacles.draw()

    for boid in boids:
        closeBoids = []                                                     #new list
        for otherBoid in boids:
            if otherBoid == boid: continue
            distance = boid.pos.distance_to(otherBoid.pos)
            if distance < 60:                                               # sets distance for creating list
                closeBoids.append(otherBoid)
                #closeBoids.nudge - endre velocity pitte litt
                
        for farBoids in closeBoids:
            if farBoids == boid: continue
            distance = boid.pos.distance_to(farBoids.pos)
            if distance > 70:                                               # sets distance for removing from list
                closeBoids.remove(farBoids)
        
        

        

        boid.cohesion(closeBoids)
        boid.alignment(closeBoids)  
        boid.separation(closeBoids) 
        boid.nudge(closeBoids)
        boid.border()
        #boid.avvoid_obs(obstacles_list)

        boid.move()
 
    
    for boid in boids:
        boid.update()
    
    for hoik in hoiks:
        huntteam = []                                                       # new list                                                 
        for otherHoik in hoiks:
            if otherHoik == hoik: continue
            distance = hoik.pos.distance_to(otherHoik.pos)
            if distance < 100:                                              # sets distance for creating a list
                huntteam.append(otherHoik)

        
        hoik.border()
        hoik.cohesion(huntteam)
        hoik.separation(huntteam)
        hoik.alignment(huntteam)
        hoik.nudge(huntteam)
        hoik.move()
        hoik.update()
        
        
    
    pygame.display.flip()
    pygame.time.delay(10)


    
    pygame.display.update()  

        

pygame.quit()  