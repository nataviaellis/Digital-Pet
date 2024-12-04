python project.pyimport random
import pygame


class Particle:
    def __init__(self, pos=(0, 0), size=30, life=1000):
        self.pos = pos
        self.size = size
        self.color = pygame.Color(random.randrange(63, 244), random.randrange(0, 7), random.randrange(74, 131))
        self.age = 0  # age in milliseconds
        self.life = life  # in milliseconds
        self.dead = False
        self.alpha = 255
        self.surface = self.update_surface()

    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            self.dead = True
        else:
            self.alpha = int(255 * (1 - (self.age / self.life)))

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)  # Enable per-pixel alpha
        pygame.draw.circle(surf, self.color, (self.size // 2, self.size // 2), self.size // 2)
        return surf

    def draw(self, surface):
        if self.dead:
            return
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)


class ParticleTrail:
    def __init__(self, pos, size, life):
        self.pos = pos
        self.size = size
        self.life = life
        self.particles = []

    def update(self, dt):
        particle = Particle(self.pos, size=self.size, life=self.life)
        self.particles.insert(0, particle)
        self._update_particles(dt)
        self._update_pos()

    def _update_particles(self, dt):
        for idx, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.dead:
                del self.particles[idx]

    def _update_pos(self):
        x, y = self.pos
        y += self.size
        self.pos = (x, y)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)


class Rain:
    def __init__(self, screen_res):
        self.screen_res = screen_res
        self.particle_size = 15
        self.birth_rate = 2  # trails per frame
        self.trails = []

    def update(self, dt):
        self._birth_new_trails()
        self._update_trails(dt)

    def _update_trails(self, dt):
        for idx, trail in enumerate(self.trails):
            trail.update(dt)
            if self._trail_is_offscreen(trail):
                del self.trails[idx]

    def _trail_is_offscreen(self, trail):
        if len(trail.particles) > 0:
            return trail.particles[-1].pos[1] > self.screen_res[1]
        return True

    def _birth_new_trails(self):
        for count in range(self.birth_rate):
            screen_width = self.screen_res[0]
            x = random.randrange(0, screen_width, self.particle_size)
            pos = (x, 0)
            life = random.randrange(500, 3000)
            trail = ParticleTrail(pos, self.particle_size, life)
            self.trails.insert(0, trail)

    def draw(self, surface):
        for trail in self.trails:
            trail.draw(surface)


class DigitalPet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw_pet(self, surface):
        # Body
        pygame.draw.ellipse(surface, (255, 149, 0), (self.x - 50, self.y - 50, 100, 100))

        # Ears
        pygame.draw.polygon(surface, (255, 149, 0), [(self.x - 47, self.y - 10), (self.x - 15, self.y - 48), (self.x - 45, self.y - 85)])
        pygame.draw.polygon(surface, (255, 149, 0), [(self.x + 47, self.y - 10), (self.x + 15, self.y - 48), (self.x + 45, self.y - 85)])

        # Inner Ears
        pygame.draw.polygon(surface, (255, 0, 0), [(self.x - 40, self.y - 34), (self.x - 25, self.y - 48), (self.x - 40, self.y - 68)])
        pygame.draw.polygon(surface, (255, 0, 0), [(self.x + 40, self.y - 34), (self.x + 25, self.y - 48), (self.x + 40, self.y - 68)])

        # Eyes
        pygame.draw.ellipse(surface, (255, 255, 255), (self.x - 44, self.y - 30, 49, 44))
        pygame.draw.ellipse(surface, (255, 255, 255), (self.x + 4, self.y - 30, 49, 44))
        
        pygame.draw.ellipse(surface, (0, 0, 0), (self.x - 30, self.y - 20, 25, 25))
        pygame.draw.ellipse(surface, (0, 0, 0), (self.x + 20, self.y - 20, 25, 25))

        pygame.draw.ellipse(surface, (255, 255, 255), (self.x - 25, self.y - 15, 13, 13))
        pygame.draw.ellipse(surface, (255, 255, 255), (self.x - 32, self.y - 18, 9, 9))
        

        # Nose
        pygame.draw.polygon(surface, (247, 148, 148), [(self.x - 12, self.y + 15), (self.x + 12, self.y + 15), (self.x, self.y + 25)])

        # Mouth
        pygame.draw.arc(surface, (255, 0, 0), (self.x - 15, self.y + 20, 30, 20), 3.14, 2 * 3.14, 2)

        # Whiskers
        pygame.draw.line(surface, (0, 0, 0), (self.x - 55, self.y + 22), (self.x - 32, self.y + 22), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x + 55, self.y + 22), (self.x + 32, self.y + 22), 2)


def main():
    pygame.init()
    pygame.display.set_caption("Digital Pet")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)  # Display size
    screen = pygame.display.set_mode(resolution)

    rain = Rain(resolution)
    pet = DigitalPet(400, 300) #center
    running = True

    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse clicks
                rain.birth_rate = min(rain.birth_rate + 1, 5)  # Cap the birth rate at 10

        # Game logic
        rain.update(dt)

        # Render and Display
        background = pygame.Color(112, 50, 153)
        screen.fill(background)
        rain.draw(screen)
        pet.draw_pet(screen)  # Call the draw_pet method with the screen as the surface
        pygame.display.flip()

        dt = clock.tick(30)  # Limit the frame rate to 30 FPS

    pygame.quit()


if __name__ == "__main__":
    main()