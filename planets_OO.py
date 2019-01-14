import pygame
import math
class Orb:
    def __init__(self, center_x, center_y, radius, color):
        self.center_y = center_y
        self.center_x = center_x
        self.radius = radius
        self.color = color
        self.anchor = None

    def draw(self, screen, dx, dy):
        pygame.draw.circle(screen, self.color, (int(self.center_x + dx), int(self.center_y + dy)), self.radius, 0)




class OrbitingOrb(Orb):
    def __init__(self, center_x, center_y, radius, color, speed, anchor):
        Orb.__init__(self, center_x, center_y, radius, color)
        self.speed = speed
        self.anchor = anchor

    def rotate(self):
        if self.anchor.anchor:
            self.rotateAroundPoint(self.anchor.anchor.center_x, self.anchor.anchor.center_y, self.anchor.speed)

        self.rotateAroundPoint(self.anchor.center_x, self.anchor.center_y, self.speed)

        

        

    
    def rotateAroundPoint(self, origin_x, origin_y, angle):
        translated_point_x = self.center_x - origin_x
        translated_point_y = self.center_y - origin_y
        rotated_x = math.cos(angle) * translated_point_x - math.sin(angle) * translated_point_y
        rotated_y = math.sin(angle) * translated_point_x + math.cos(angle) * translated_point_y
        self.center_x = rotated_x + origin_x
        self.center_y = rotated_y + origin_y        


class Game:
    
    def __init__(self):
        self.SCREEN_SIZE_X = 1440
        self.SCREEN_SIZE_Y = 810

        self.SCREEN_HALF_X = int(self.SCREEN_SIZE_X / 2)
        self.SCREEN_HALF_Y = int(self.SCREEN_SIZE_Y / 2)

        sun_center_x = self.SCREEN_HALF_X
        sun_center_y = self.SCREEN_HALF_Y
        sun_radius = 140
        self.sun = Orb(sun_center_x, sun_center_y, sun_radius, (150, 100, 0))


        earth_radius = 20
        earth_orbiting_speed = 0.001
        earth_center_x = sun_center_x + 250
        earth_center_y = sun_center_y
        self.earth = OrbitingOrb(earth_center_x, earth_center_y, earth_radius, (0, 100, 200), earth_orbiting_speed, self.sun)

        moon_radius = 4
        moon_orbiting_speed = 0.0012
        moon_center_x = earth_center_x + 50
        moon_center_y = sun_center_y
        self.moon = OrbitingOrb(moon_center_x, moon_center_y, moon_radius, (100, 100, 150), moon_orbiting_speed, self.earth)


        jupiter_center_x = sun_center_x + 400
        jupiter_center_y = sun_center_y
        jupiter_radius = 40
        jupiter_orbiting_speed = 0.0003
        self.jupiter = OrbitingOrb(jupiter_center_x, jupiter_center_y, jupiter_radius, (200, 150, 150), jupiter_orbiting_speed, self.sun)

        jupiter_moon_radius = 10
        jupiter_moon_orbiting_speed = 0.003
        jupiter_moon_center_x = jupiter_center_x + 77
        jupiter_moon_center_y = sun_center_y
        self.jupiter_moon = OrbitingOrb(jupiter_moon_center_x, jupiter_moon_center_y, jupiter_moon_radius, (50, 150, 50), jupiter_moon_orbiting_speed, self.jupiter)

        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE_X, self.SCREEN_SIZE_Y))
        self.orbs = [self.sun]
        self.orbiting_orbs = [self.earth, self.moon, self.jupiter, self.jupiter_moon]        
        self.view = self.sun
    def drawPlanets(self, dx, dy):
        for p in (self.orbs + self.orbiting_orbs):
            p.draw(self.screen, dx, dy)
                          
    def rotatePlanets(self):
        for o in self.orbiting_orbs:
            o.rotate()

    
    def whichPlanetIsCloser(self, click_x, click_y, dx, dy ):
        click_x -= dx
        click_y -= dy
        closest_planet = self.sun
        minimum_hamming_distance = 20000
        for o in self.orbiting_orbs + self.orbs:
            if click_x > o.center_x:
                distance_x = click_x - o.center_x
            else:
                distance_x = o.center_x - click_x
            if click_y > o.center_y:
                distance_y = click_y - o.center_y
            else:
                distance_y = o.center_y - click_y
            hamming_distance = distance_x + distance_y

            if hamming_distance < minimum_hamming_distance:
                minimum_hamming_distance = hamming_distance
                closest_planet = o

        return closest_planet



    def shift(self, dx, dy):           
        movement_x = dx / 600
        movement_y = dy / 600
        speed1 = 1
        speed2 = 1
        movement_so_far = 0
        if movement_so_far < 300:
            for p in (self.orbs + self.orbiting_orbs):
                p.draw(self.screen, int(movement_x * speed1 * speed2), int(movement_y * speed1 * speed2))
                movement_so_far += speed1 * speed2
                speed1 += 1
                speed2 += 1

        elif movement_so_far < 600:
            for p in (self.orbs + self.orbiting_orbs):
                p.draw(self.screen, int(movement_x * speed1 * speed2), int(movement_y * speed1 * speed2))
                movement_so_far += speed1 * speed2
                speed1 -= 1
                speed2 -= 1
  



    def run(self):
        running = True
        exiting = False
        view_shift = False
        movement = 1
        while not exiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exiting = True
                if event.type ==  pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = not running
                if event.type == pygame.MOUSEBUTTONDOWN:
                    view_shift = True
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    old_distance_x = self.sun.center_x - self.view.center_x
                    old_distance_y = self.sun.center_y - self.view.center_y                    
                    distance_x = self.sun.center_x - self.view.center_x
                    distance_y = self.sun.center_y - self.view.center_y
                    old_view = self.view
                    self.view = self.whichPlanetIsCloser(mouse_x, mouse_y, distance_x, distance_y)
                    pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.SCREEN_SIZE_X, self.SCREEN_SIZE_Y), 0)
                    # self.shift(distance_x, distance_y)
            if running:
                distance_x = self.sun.center_x - self.view.center_x
                distance_y = self.sun.center_y - self.view.center_y

                pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.SCREEN_SIZE_X, self.SCREEN_SIZE_Y), 0)
                self.rotatePlanets()

                if view_shift:
                    self.rotatePlanets()
                    if old_view != self.sun:
                        distance_x = self.sun.center_x - self.view.center_x
                        distance_y = self.sun.center_y - self.view.center_y
                        self.drawPlanets(old_distance_x + (distance_x - old_distance_x) / 600 * movement, old_distance_y + (distance_y - old_distance_y) / 600 * movement)
                    else:
                        distance_x = self.sun.center_x - self.view.center_x
                        distance_y = self.sun.center_y - self.view.center_y
                        self.drawPlanets(distance_x / 600 * movement, distance_y / 600 * movement)
                    movement += 1
                    if movement == 600:
                        view_shift = False
                        
                else:
                    self.drawPlanets(distance_x, distance_y)
                    movement = 1
            pygame.display.flip()


game = Game()
game.run()

