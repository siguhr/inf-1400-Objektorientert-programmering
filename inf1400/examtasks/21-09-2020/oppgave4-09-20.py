import pygame
import random


####
# Configuration
####

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
STEPS_PER_SECOND = 30

INFECTION_RANGE = 40
RECOVERY_TIME = 5
SYKEBIL_SPEED = 2

MOVEMENT_RANGE = 5
NUMBER_OF_PEOPLE = 100

INFECTION_MB_RANGE = 10                      # Ny global!
INFECTION_MBx2_RANGE = 5

####
# List and weights of behaviors and status
# Weights are relative (e.g. susceptible is 10 times more likely than infected)
####
behaviors = ["surrehode", "sykebil", "MBsurrehode"]                        # ny adferd
behavior_weight = [10, 1, 10]                                              # ny ratio
status = ["infected", "susceptible", "recovered"]
status_weight = [1, 10, 0]


class Objects():
    def __init__(self):
        self.color
        self.movement_x
        self.movement_y
        self.pos_x
        self.pos_y


    def move(target, others):
        '''
        Move the target based on the behavior
        target - the person to move
        others - list of all other persons
        returns nothing
        modifies the position of target
        '''
        if target["behavior"] == "surrehode, MBsurrehode":                  #ny kode
            movement_x = random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)
            movement_y = random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)
            movement_vector = pygame.math.Vector2(movement_x, movement_y)
            target["position"] += movement_vector
            if target["position"].x < 0:
                target["position"].x = SCREEN_WIDTH + target["position"].x
            if target["position"].x > SCREEN_WIDTH:
                target["position"].x = target["position"].x % SCREEN_HEIGHT
            if target["position"].y < 0:
                target["position"].y = SCREEN_HEIGHT + target["position"].y
            if target["position"].y > SCREEN_HEIGHT:
                target["position"].y = target["position"].y % SCREEN_HEIGHT
        if target["behavior"] == "sykebil":
            t = find_closest_infected(target, others)
            if t is None:
                return
            difference_vector = t["position"] - target["position"]
            try:
                movement_direction = difference_vector.normalize()
            except ValueError:
                movement_direction = pygame.math.Vector2(0, 0)
            target["position"] += movement_direction * SYKEBIL_SPEED

        


    def update_infection_status(target, others):
        '''
        spreads, cures or recovers infections
        target - the person who is spreading or recovering
        other - list of all other persons
        returns nothing
        modifies target's and other's status
        '''

        if target["behavior"] == "MBsurrehode":                                         # ny! Hvis person bruker munnbind
            if target["status"] == "infected":                                          # Likt forløp ved smitte
                target["sick_time"] += 1
                if target["sick_time"] > RECOVERY_TIME * STEPS_PER_SECOND:
                    target["status"] = "recovered"
                for other in others:
                    distance = target["position"].distance_to(other["position"])
                    if distance < INFECTION_RANGE:                                     # Hvis avstannd er mindre enn normal infeksjon avstand!
                        if other["behavior"] == "sykebil":                                
                            target["status"] = "recovered"
                        elif other["status"] == "susceptible":                            
                            other["status"] = "susceptible"
                        
                        if other["behavior"] == "MBsurrehode":                            # Hvis person med munnbind møter "annen" med munnbind
                            if distance < INFECTION_MB_RANGE:
                                if other["status"] == "susceptible":                     # Normal infection avstand for to munnbindbrukere gir ikke smitte
                                    target["status"] = "susceptible"
                            elif distance < INFECTION_MBx2_RANGE:                        # Hvis avstannd er mindre enn MBx2 radius mellom to munnbindbrukere..
                                if other["status"] == "susceptible":
                                    target["status"] = "infected"                       # Gir smitte
        
        if target["behavior"] == "surrehode":                                           # Hvis person ikke bruker munnbind
            if target["status"] == "infected":                                          # Lik forløp hvis smittet
                target["sick_time"] += 1
                if target["sick_time"] > RECOVERY_TIME * STEPS_PER_SECOND:
                    target["status"] = "recovered"
                for other in others:
                    distance = target["position"].distance_to(other["position"])
                    if distance < INFECTION_RANGE:                                      # Hvis avstannd er mindre enn normal infection avstand..
                        if other["behavior"] == "sykebil":
                            target["status"] = "recovered"
                        elif other["status"] == "susceptible":
                            other["status"] = "infected"

                        if other["behavior"] == "MBsurrehode":                          # Hvis person uten munnbind møter "annen" med munnbind.
                            if distance < INFECTION_RANGE:
                                if other["status"] == "susceptible":                    # Normal infection avstand gir ikke smitte
                                    target["status"] = "susceptible"
                            elif distance < INFECTION_MB_RANGE:                         # Hvis avstannd er mindre enn MB avstand.
                                if other["status"] == "susceptible":    
                                    target["status"] = "infected"                       # Gir smitte
    def draw(target):
        '''
        draw the target on screen
        target - the person to draw on screen
        color and shape are determined by status and behavior of the target
        image is drawn on global variable screen
        returns nothing
        '''


        if target["status"] == "infected":
            color = (255, 0, 0)
        elif target["status"] == "susceptible":
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        if target["behavior"] == "MBsurrehode":         #ny farge for munnbind-surrehoder
            color = (0, 255, 255)
        if target["behavior"] == "sykebil":
            r = pygame.Rect((0, 0, 15, 15))
            r.center = target["position"]
            pygame.draw.rect(screen, color, r)
        else:
            x = int(target["position"].x)
            y = int(target["position"].y)
            pygame.draw.circle(screen, color, (x, y), 10)


    def make_person():
        '''
        make a new random person
        returns a person with random attributes, based on the weights
        of each attribute
        behavior "sykebil" is always status "recovered"
        '''
        result = {}
        pos_x = random.randint(0, SCREEN_WIDTH)
        pos_y = random.randint(0, SCREEN_HEIGHT)
        result["position"] = pygame.math.Vector2(pos_x, pos_y)
        result["behavior"] = random.choices(behaviors, behavior_weight)[0]
        result["status"] = random.choices(status, status_weight)[0]
        if result["behavior"] == "sykebil":
            result["status"] = "recovered"
        result["sick_time"] = 0
        return result


class sykebil(Objects):
    def __init__(self):
        super().__init__()

    
    def find_closest_infected(target, others):
        '''
        Get the closest infected person from list
        target - the person we are finding the closest person to
        other - list of all other persons
        returns the element from others which is closest to the target
        '''
        pos = target["position"]

        min_distance = 1000
        closest = None
        for other in others:
            if other == target:
                # no need to investigate distance to self
                continue
            if other["status"] == "infected":
                distance = target["position"].distance_to(other["position"])
                if distance < min_distance and distance != 0:
                    min_distance = distance
                    closest = other
        return closest

class surrehode (Objects):
    def __init__(self):
        super().__init__()

class MBsurrehode (Objects):
    def __init__(self):
        super().__init__()


####
# main loop
# set up screen, and perform the main loop of the simulation
####
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    people = []
    for _ in range(NUMBER_OF_PEOPLE):
        people.append(make_person())
    clock = pygame.time.Clock()
    while True:
        clock.tick(STEPS_PER_SECOND)
        screen.fill((0, 0, 0))
        for p in people:
            update_infection_status(p, people)
            move(p, people)
            draw(p)
        pygame.display.flip()



