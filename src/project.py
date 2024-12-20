import random
import pygame

class Particle:
    def __init__(self, pos=(0, 0), size=500, life=500):
        self.pos = pos
        self.size = size
        self.color = pygame.Color(255, 255, 255)
        self.age = 0  # age in milliseconds
        self.life = life  # in milliseconds
        self.dead = False
        self.alpha = 5
        self.surface = self.update_surface()

    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            self.dead = True
        else:
            self.alpha = int(20 * (1 - (self.age / self.life)))

    def update_surface(self):
        size = self.size
        surf = pygame.Surface((size, size // 2), pygame.SRCALPHA)  # Enable per-pixel alpha
        
        # Draw cat shape
        pygame.draw.circle(surf, self.color, (size // 4, size // 4), size // 4)
        pygame.draw.circle(surf, self.color, (3 * size // 4, size // 4), size // 4)
        pygame.draw.rect(surf, self.color, (size // 4, size // 4, size // 2, size // 4))
        
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
        self.particle_size = 25
        self.birth_rate = 1  # trails per frame
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
        self.dragging = False  # Track if the pet is being dragged
        self.offset_x = 0
        self.offset_y = 0

    def draw_pet(self, surface):
        # Head
        pygame.draw.circle(surface, (255, 149, 0), (self.x, self.y - 7), 50)

        # White part of fur
        pygame.draw.ellipse(surface, (255, 255, 255), (self.x - 60, self.y - 10, 120, 80))

        # Ears
        pygame.draw.polygon(surface, (255, 149, 0), [(self.x - 47, self.y - 10), (self.x - 15, self.y - 48), (self.x - 45, self.y - 85)])
        pygame.draw.polygon(surface, (255, 149, 0), [(self.x + 47, self.y - 10), (self.x + 15, self.y - 48), (self.x + 45, self.y - 85)])

        pygame.draw.polygon(surface, (255, 0, 0), [(self.x - 40, self.y - 25), (self.x - 10, self.y - 48), (self.x - 45, self.y - 85)])
        pygame.draw.polygon(surface, (255, 0, 0), [(self.x + 40, self.y - 25), (self.x + 10, self.y - 48), (self.x + 45, self.y - 85)])

        # Brown Part of eye
        pygame.draw.ellipse(surface, (150, 109, 32), (self.x - 55, self.y - 25, 49, 44))
        pygame.draw.ellipse(surface, (150, 109, 32), (self.x + 5, self.y - 25, 49, 44))

        # White Part of Eye
        pygame.draw.ellipse(surface, (255, 255, 255), (self.x - 45, self.y - 25, 45, 45))
        pygame.draw.ellipse(surface, (255, 255, 255), (self.x, self.y - 25, 45, 45))

        # Black Part of Eye
        pygame.draw.ellipse(surface, (0, 0, 0), (self.x - 29, self.y - 10, 25, 25))
        pygame.draw.ellipse(surface, (0, 0, 0), (self.x + 10, self.y - 10, 25, 25))

        # Nose
        pygame.draw.polygon(surface, (247, 148, 148), [(self.x - 12, self.y + 15), (self.x + 10, self.y + 15), (self.x, self.y)])

        # Whiskers 
        pygame.draw.line(surface, (0, 0, 0), (self.x - 55, self.y + 22), (self.x - 32, self.y + 22), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x + 50, self.y + 22), (self.x + 30, self.y + 22), 2)

        # Mouth
        pygame.draw.ellipse(surface, (138, 32, 32), (self.x - 20, self.y + 25, 40, 35))

        # Tongue
        pygame.draw.ellipse(surface, (250, 147, 147), (self.x - 15, self.y + 50, 28, 10))

    def handle_mouse_down(self, pos):
        # Check if the pet is clicked
        if (self.x - 50 <= pos[0] <= self.x + 50) and (self.y - 50 <= pos[1] <= self.y + 50):
            self.dragging = True
            self.offset_x = pos[0] - self.x
            self.offset_y = pos[1] - self.y

    def handle_mouse_up(self):
        self.dragging = False

    def update_position(self, pos, screen_width, screen_height):
        if self.dragging:
            new_x = pos[0] - self.offset_x
            new_y = pos[1] - self.offset_y
            
            # Prevent the pet from going outside the screen boundaries
            if new_x < 50:  # Prevent going out on the left
                new_x = 50
            elif new_x > screen_width - 50:  # Prevent going out on the right
                new_x = screen_width - 50

            if new_y < 50:  # Prevent going out on the top
                new_y = 50
            elif new_y > screen_height - 50:  # Prevent going out on the bottom
                new_y = screen_height - 50

            self.x = new_x
            self.y = new_y


def main():
    pygame.init()
    pygame.display.set_caption("Digital Pet")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)  # Display size
    screen = pygame.display.set_mode(resolution)

    rain = Rain(resolution)
    pet = DigitalPet(400, 300)  # center
    running = True

    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse clicks
                pet.handle_mouse_down(event.pos)  # Handle the pet dragging
                rain.birth_rate = min(rain.birth_rate + 1, 5)  # Cap the birth rate at 5
            elif event.type == pygame.MOUSEBUTTONUP:  # Handle mouse button release
                pet.handle_mouse_up()
            elif event.type == pygame.MOUSEMOTION:  # Handle mouse motion
                pet.update_position(event.pos, resolution[0], resolution[1])

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